# pylint: disable=C0114, C0115, C0116
# coding: utf-8

# TODO
# MariaDB의 디스크 관리를 위해 주기적으로 History 데이터를 삭제해줘야 한다.

import os
import sys
from platform import node, platform

from prefect import context, flow, get_run_logger
from prefect.runtime import flow_run
from prefect.task_runners import SequentialTaskRunner
from yaml import YAMLError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.common.base_impl import sql_delete_metric_eval_history
from common_modules.common.util import create_basetime, get_after_days
from common_modules.config.yaml_config import YamlConfig
from common_modules.db.mariadb.conn import MariaDBConnection
from common_modules.define.name import (BASE_CONFIG_PATH,
                                        MARIADB_AFTER_DAYS_NAME,
                                        MARIADB_SCHEDULER_NAME)


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
    name=MARIADB_SCHEDULER_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="Prefect agent module for clean up mariadb",
    timeout_seconds=5,
    task_runner=SequentialTaskRunner(),
)
def mariadb_cleanup_flow() -> None:
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

    mariadb_connection = MariaDBConnection(
        logger, *yaml_config.get_all_config().get("MARIADB").values()
    )

    deleted_rows = mariadb_connection.execute_session_query(
        sql_delete_metric_eval_history, get_after_days(MARIADB_AFTER_DAYS_NAME)
    )

    logger.info(f"Deleted rows : {deleted_rows}")

    # TODO t_alert_history 삭제 로직 추가


if __name__ == "__main__":
    mariadb_cleanup_flow()
