# pylint: disable=C0114, C0115, C0116
# coding: utf-8

# TODO
# events, event_resources의 경우 신규로 생긴 테이블로 이벤트에 대한 기록을 한다.
# flow 동작에 따라 데이터가 쌓이는 경우 해당 테이블 역시 삭제 쿼리를 넣어 정리 할 피필요가 힜다.

import os
import sys
from platform import node, platform

from prefect import context, flow, get_run_logger
from prefect.runtime import flow_run
from sqlalchemy import delete
from yaml import YAMLError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.config.yaml import YamlConfig
from app.core.db.postgresql.conn import PostgreSQLConnection
from app.core.db.postgresql.prefect_base import Artifact, FlowRun, Log
from app.core.define.base import Path
from app.core.define.flows import PostgreSQLManager
from app.core.define.prefect import Variables
from app.utils.prefect import get_after_days
from app.utils.time import create_basetime


def generate_flow_run_name() -> str:
    logger = get_run_logger()

    flow_run_name_datetime = create_basetime(
        logger, context.get_run_context().flow_run.expected_start_time
    )
    flow_run_name = f"{flow_run.get_flow_name()}-{flow_run_name_datetime:%Y%m%d}-{flow_run_name_datetime:%H%M%S}"

    logger.info(
        "flow_run_id: %s, flow_run_deployment_id: %s, flow_run_name: %s ✅",
        context.get_run_context().flow_run.flow_id,
        context.get_run_context().flow_run.deployment_id,
        flow_run_name,
    )

    return flow_run_name


@flow(
    name=PostgreSQLManager.Flows.POSTGRES_CLEAN_FLOW_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="""Prefect worker for cleanup postgresql.
                    We adopt a strict Vacuum policy to optimize disk space utilization for the table.
    """,
    timeout_seconds=5,
)
def postgres_clean_flow() -> None:
    logger = get_run_logger()

    logger.info("Network: %s. ✅", node())
    logger.info("Instance: %s. ✅", platform())

    try:
        yaml_config = YamlConfig(
            logger=logger, config_path=Path.CONFIG_PATH + "/config_dev.yml"
        )
    except FileNotFoundError as err:
        logger.error("File Not Found : %s", str(err))
        raise
    except YAMLError as err:
        logger.error("Yaml load Error : %s", str(err))
        raise

    postgres_connection = PostgreSQLConnection(
        logger, *yaml_config.get_all_config().get("POSTGRESQLDB").values()
    )

    with postgres_connection.get_session() as session:
        x_days_before = get_after_days(Variables.X_DAYS_BEFORE).strftime("%Y-%m-%d")
        old_flow_run_ids = (
            session.query(FlowRun.id)
            .filter(
                FlowRun.state_timestamp < x_days_before,
                FlowRun.state_type == "COMPLETED",
            )
            .all()
        )

        if not old_flow_run_ids:
            logger.info("No old flow_run records found for cleanup.")
            return

        flow_run_ids = [flow_run.id for flow_run in old_flow_run_ids]

        delete_queries = [
            delete(Log).where(Log.flow_run_id.in_(flow_run_ids)),
            delete(Artifact).where(Artifact.flow_run_id.in_(flow_run_ids)),
            delete(FlowRun).where(FlowRun.id.in_(flow_run_ids)),
        ]

        for query in delete_queries:
            session.execute(query)

        session.commit()

        logger.info(
            f"Deleted {len(flow_run_ids)} old flow_runs and related logs & artifacts, events"
        )


if __name__ == "__main__":
    postgres_clean_flow()
