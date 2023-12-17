# pylint: disable=C0114, C0115, C0116
# coding: utf-8


import os
import sys
from platform import node, platform

from prefect import context, flow, get_run_logger
from prefect.runtime import flow_run
from prefect.task_runners import SequentialTaskRunner
from requests import exceptions
from yaml import YAMLError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.alert.api import alert_send_api
from common_modules.alert.slack import flow_failure_webhook
from common_modules.common.base_impl import (
    Metric,
    sql_get_metric_eval_threshold_list,
    sql_insert_alert_history,
    sql_insert_metric_eval_history,
)
from common_modules.common.util import create_basetime, update_point
from common_modules.config.yaml_config import YamlConfig
from common_modules.data.comparison_operator import OperatorMapping
from common_modules.data.data_velidator import verify_data
from common_modules.db.influxdb.conn import InfluxDBConnection
from common_modules.db.mariadb.conn import MariaDBConnection
from common_modules.db.mariadb.metric_watcher_base import TCodeMetricEvalResultType
from common_modules.define.code import EvalResultType, EvalType, MetricType
from common_modules.define.name import (
    BASE_CONFIG_PATH,
    METRIC_DISK_ROOT_SCHEDULER_NAME,
    POINT_USED_PERCENT,
)

# Lazy Query 수행 (1분 이내로 데이터 입수가 가능하지 않을 수도 있으므로)
GET_DISK_ROOT_USED_PERCENT_QUERY = """SELECT time, host, used_percent FROM disk 
    WHERE time > now() - 2m and path = '/' group by host limit 1"""


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
    name=METRIC_DISK_ROOT_SCHEDULER_NAME,
    flow_run_name=generate_flow_run_name,
    retries=1,
    retry_delay_seconds=5,
    description="Prefect agent module for Disk root usage",
    timeout_seconds=5,
    task_runner=SequentialTaskRunner(),
    on_failure=[flow_failure_webhook],
)
def metric_disk_root_flow() -> None:
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

    influx = InfluxDBConnection(
        logger, *yaml_config.get_all_config().get("INFLUXDB").values()
    )

    # InfluxDB 데이터 조회
    with influx.get_resource() as conn:
        try:
            results = conn.query(GET_DISK_ROOT_USED_PERCENT_QUERY)
        except exceptions.ConnectionError as err:
            logger.error("Connection Error : %s", str(err))
            raise

        metric_points = results.get_points()

    # MariaDB 조회 및 InfluxDB 데이터 평가
    mariadb_connection = MariaDBConnection(
        logger, *yaml_config.get_all_config().get("MARIADB").values()
    )

    eval_common_list = mariadb_connection.execute_session_query(
        sql_get_metric_eval_threshold_list,
        MetricType.DISK_ROOT.value,
        EvalType.COMMON.value,
    )

    metric_disk_root = None

    for common in eval_common_list:
        metric_disk_root = Metric(*common)

    if not verify_data(logger, metric_disk_root):
        # TODO Alert 발송 (Slack)
        return
    else:
        for point in metric_points:
            eval_result_value = EvalResultType.OK.value

            if OperatorMapping.get(metric_disk_root.eval_operator_type_seq).compare(
                point.get("used_percent"), metric_disk_root.eval_value
            ):
                eval_result_value = EvalResultType.ALERT.value

            update_point(
                point,
                metric_disk_root,
                TCodeMetricEvalResultType.metric_eval_result_seq.name,
                eval_result_value,
            )

            print("Point =>", point)  # Local logging

    print("metric_disk_root =>", metric_disk_root)

    # TODO Alert 발송
    for eval_point in metric_disk_root.eval_point_group_list:
        # TODO 관제 해야 할 서버의 개수가 많아질 경우 session.add_all로 변경 필요할 수도..
        with mariadb_connection.get_resources() as session:
            sql_insert_metric_eval_history(
                mariadb_connection,
                session,
                metric_disk_root.metric_eval_threshold_seq,
                eval_point,
                POINT_USED_PERCENT,
            )

        # alert_history에 결과 등록 필요
        if (
            eval_point.get(TCodeMetricEvalResultType.metric_eval_result_seq.name)
            > EvalResultType.OK.value
        ):
            if (
                eval_point.get(TCodeMetricEvalResultType.metric_eval_result_seq.name)
                == EvalResultType.ALERT.value
            ):
                generated_messages, alert_send_result = alert_send_api(
                    metric_disk_root, eval_point
                )
                sql_insert_alert_history(session, generated_messages, alert_send_result)

            elif (
                eval_point.get(TCodeMetricEvalResultType.metric_eval_result_seq.name)
                == EvalResultType.SNOOZE.value
            ):
                pass


if __name__ == "__main__":
    metric_disk_root_flow()
