# pylint: disable=C0114, C0115, C0116
# coding: utf-8

import logging
import os
import sys
from platform import node, platform

from prefect import cache_policies, context, flow, get_run_logger, task
from prefect.runtime import flow_run

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.config.yaml import get_yaml_config
from app.core.db.mariadb.connector import MariaDBConnector
from app.core.define.base import Path
from app.core.define.flows import MariaDBManager
from app.core.define.prefect import Variables
from app.core.define.tasks import MariadbClean
from app.core.impls.metric import sql_delete_evaluate_result_history
from app.utils.prefect import get_before_days
from app.utils.time import create_basetime, get_run_datetime


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


@task(
    name=MariadbClean.Tasks.CLEANUP_MARIADB_TABLES_NAME,
    task_run_name=f"{MariadbClean.Tasks.CLEANUP_MARIADB_TABLES_NAME}_{get_run_datetime()}",
    retries=3,
    retry_delay_seconds=5,
    cache_policy=cache_policies.NO_CACHE,
    description="Cleanup mariadb tables",
)
def cleanup_mariadb_tables(
    logger: logging.Logger, mariadb_connector: MariaDBConnector
) -> None:
    deleted_rows = mariadb_connector.execute_session_query(
        sql_delete_evaluate_result_history, get_before_days(Variables.X_DAYS_BEFORE)
    )

    logger.info(f"Deleted rows : {deleted_rows}")


@flow(
    name=MariaDBManager.Flows.MARIADB_CLEAN_FLOW_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="Prefect agent module for clean up mariadb",
    timeout_seconds=5,
)
def mariadb_clean_flow() -> None:
    logger = get_run_logger()

    logger.info("Network: %s. ✅", node())
    logger.info("Instance: %s. ✅", platform())

    yaml_config = get_yaml_config(logger, Path.CONFIG_PATH)

    mariadb_connector = MariaDBConnector(logger, **yaml_config.mariadb.model_dump())

    cleanup_mariadb_tables(logger, mariadb_connector)

    logger.info("Cleanup mariadb tables. ✅")


if __name__ == "__main__":
    mariadb_clean_flow()
