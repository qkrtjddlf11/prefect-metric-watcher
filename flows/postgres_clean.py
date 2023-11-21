# pylint: disable=C0114, C0115, C0116
# coding: utf-8

# TODO Prefect의 로그는 PostgreSQL에 저장되며, 주기적으로 삭제해주는 로직이 없어 직접 삭제를 수행해줘야 한다.
# 테이블의 디스크 용량 확보를 위해 타이트한 Vacuum 정책을 가져간다.
import os
import sys
from platform import node, platform

import psycopg2
from prefect import context, flow, get_run_logger
from prefect.runtime import flow_run
from prefect.task_runners import SequentialTaskRunner
from yaml import YAMLError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.common.util import create_basetime, get_after_days
from common_modules.config.yaml_config import YamlConfig
from common_modules.db.postgresql.conn import PostgreSQLConnection

BASE_CONFIG_PATH = "config/config_dev.yaml"
POSTGRES_SCHEDULER_NAME = "prefect_metric_cpu_scheduler"
PREFECT_POSTGRES_AFTER_DAYS_NAME = "prefect_postrgres_after_days"


def generate_flow_run_name() -> str:
    logger = get_run_logger()

    flow_run_name_datetime = create_basetime(
        logger, context.get_run_context().flow_run.expected_start_time
    )
    flow_run_name = f"{flow_run.flow_name}-{flow_run_name_datetime:%Y%m%d}-{flow_run_name_datetime:%H%M%S}"

    logger.info(
        "flow_run_id: %s, flow_run_deployment_id: %s, flow_run_name: %s ✅",
        context.get_run_context().flow_run.flow_id,
        context.get_run_context().flow_run.deployment_id,
        flow_run_name,
    )

    return flow_run_name


@flow(
    name=POSTGRES_SCHEDULER_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="Prefect agent module for CPU usage",
    timeout_seconds=5,
    task_runner=SequentialTaskRunner(),
)
def postgres_cleanup_flow() -> None:
    logger = get_run_logger()

    logger.info("Network: %s. ✅", node())
    logger.info("Instance: %s. ✅", platform())

    try:
        yaml_config = YamlConfig(logger=logger, config_path=BASE_CONFIG_PATH)
    except FileNotFoundError as err:
        logger.error("File Not Found : %s", str(err))
        raise
    except YAMLError as err:
        logger.error("Yaml load Error : %s", str(err))
        raise

    postgres_connection = PostgreSQLConnection(
        logger, *yaml_config.get_all_config().get("POSTGRESQLDB").values()
    )

    with postgres_connection.get_resources() as (cursor, conn):
        select_query = f"""
        SELECT id FROM flow_run
        WHERE state_timestamp < to_timestamp('{get_after_days(PREFECT_POSTGRES_AFTER_DAYS_NAME).strftime("%Y%m%d")}', 'YYYYMMDD')
        AND state_type = 'COMPLETED'
        """

        logger.info(f"Will be executed : {select_query}")

        try:
            cursor.execute(select_query)
            flow_ids = [flow_id[0] for flow_id in cursor.fetchall()]
            print(flow_ids)
            # if len(flow_ids) > 0:
            #     # Create the IN clause with placeholders
            #     placeholders = ", ".join(["%s"] * len(flow_ids))
            #     delete_query_list = [
            #         f"DELETE FROM flow_run WHERE id IN ({placeholders})",
            #         f"DELETE FROM log WHERE flow_run_id IN ({placeholders})",
            #     ]

            #     for delete_query in delete_query_list:
            #         cursor.execute(delete_query, flow_ids)
            #         conn.commit()
            #         logger.info(
            #             f"{delete_query.split(' ')[2]} table {cursor.rowcount} rows were deleted."
            #         )
        except psycopg2.Error as err:
            logger.error(f"Query execution failed. {err}")
            raise


if __name__ == "__main__":
    postgres_cleanup_flow()
