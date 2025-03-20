# pylint: disable=C0114, C0115, C0116
# coding: utf-8

# TODO
# events, event_resources의 경우 신규로 생긴 테이블로 이벤트에 대한 기록을 한다.
# flow 동작에 따라 데이터가 쌓이는 경우 해당 테이블 역시 삭제 쿼리를 넣어 정리 할 피필요가 힜다.
import logging
import os
import sys
from platform import node, platform

from prefect import cache_policies, context, flow, get_run_logger, task
from prefect.runtime import flow_run
from sqlalchemy import delete

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.config.yaml import get_yaml_config
from app.core.db.postgresql.connector import PostgreSQLConnector
from app.core.db.postgresql.prefect_base import (
    Artifact,
    EventResources,
    Events,
    FlowRun,
    Log,
)
from app.core.define.base import Path
from app.core.define.flows import PostgreSQLManager
from app.core.define.prefect import Variables
from app.core.define.tasks import PostgresClean
from app.utils.prefect import get_before_days
from app.utils.time import create_basetime, get_run_datetime


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


@task(
    name=PostgresClean.Tasks.CLEANUP_POSTGRESQL_TABLES_NAME,
    task_run_name=f"{PostgresClean.Tasks.CLEANUP_POSTGRESQL_TABLES_NAME}_{get_run_datetime()}",
    retries=3,
    retry_delay_seconds=5,
    cache_policy=cache_policies.NO_CACHE,
    description="Cleanup mariadb tables",
)
def cleanup_postgresql_tables(
    logger: logging.Logger, postgres_connector: PostgreSQLConnector
) -> None:
    with postgres_connector.get_session() as session:
        x_days_before = get_before_days(Variables.X_DAYS_BEFORE).strftime("%Y-%m-%d")
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
            delete(Events).where(Events.created < x_days_before),
            delete(EventResources).where(EventResources.created < x_days_before),
        ]

        for query in delete_queries:
            deleted_rows = session.execute(query)
            logger.info("Deleted %s rows from %s", deleted_rows.rowcount, query.table)

        session.commit()

        logger.info(
            f"Deleted {len(flow_run_ids)} old flow_runs and related logs & artifacts, events"
        )


@flow(
    name=PostgreSQLManager.Flows.POSTGRES_CLEAN_FLOW_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="""Prefect worker for cleanup postgresql.
                    We adopt a strict Vacuum policy to optimize disk space utilization for the table.
    """,
    timeout_seconds=60,
)
def postgres_clean_flow() -> None:
    logger = get_run_logger()

    logger.info("Network: %s. ✅", node())
    logger.info("Instance: %s. ✅", platform())

    yaml_config = get_yaml_config(logger, Path.CONFIG_PATH)

    postgres_connector = PostgreSQLConnector(
        logger, **yaml_config.postgresql.model_dump()
    )

    cleanup_postgresql_tables(logger, postgres_connector)

    logger.info("Postgres cleanup flow completed. ✅")


if __name__ == "__main__":
    postgres_clean_flow()
