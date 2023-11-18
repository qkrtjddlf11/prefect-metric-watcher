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

from common_modules.common.base_impl import Metric, sql_get_metric_eval_threshold_list
from common_modules.common.util import create_basetime, update_point
from common_modules.config.yaml_config import YamlConfig
from common_modules.data.comparison_operator import OperatorMapping
from common_modules.data.data_velidator import verify_data
from common_modules.db.influxdb.conn import InfluxDBConnection
from common_modules.db.mariadb.conn import MariaDBConnection
from common_modules.db.mariadb.metric_watcher_base import TCodeMetricEvalResultType
from common_modules.define.code import EvalResultType, EvalType, MetricType

BASE_CONFIG_PATH = "config/config_dev.yaml"
METRIC_CPU_NAME = "prefect_metric_cpu_scheduler"
CPU_USAGE_PERCENT = "usage_percent"

# Lazy Query 수행 (1분 이내로 데이터 입수가 가능하지 않을 수도 있으므로)
CPU_QUERY = """SELECT time, host, (100 - usage_idle) as usage_percent
                FROM cpu 
                WHERE time > now() - 2m AND time <= now() - 1m
                GROUP BY host limit 1"""


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
    name=METRIC_CPU_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="Prefect agent module for CPU usage",
    timeout_seconds=5,
    task_runner=SequentialTaskRunner(),
)
def metric_cpu_flow() -> None:
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

    # TODO InfluxDB 데이터 조회
    with influx.get_resource() as conn:
        try:
            results = conn.query(CPU_QUERY)
        except exceptions.ConnectionError as err:
            logger.error("Connection Error : %s", str(err))
            raise

        metric_points = results.get_points()

    # TODO MariaDB 조회 및 InfluxDB 데이터 평가
    mariadb_connection = MariaDBConnection(
        logger, *yaml_config.get_all_config().get("MARIADB").values()
    )

    results = mariadb_connection.execute_sessin_query(
        sql_get_metric_eval_threshold_list, MetricType.CPU.value, EvalType.COMMON.value
    )

    for result in results:
        metric_cpu = Metric(*result)

    if not verify_data(logger, metric_cpu):
        logger.error("Invalid data : %s", metric_cpu)
    else:
        for point in metric_points:
            eval_result_value = EvalResultType.OK.value

            if OperatorMapping.get(metric_cpu.eval_operator_type_seq).compare(
                point.get("usage_percent"), metric_cpu.eval_value
            ):
                eval_result_value = EvalResultType.ALERT.value

            update_point(
                point,
                metric_cpu,
                TCodeMetricEvalResultType.metric_eval_result_seq.name,
                eval_result_value,
            )

            print("Point =>", point)  # Local logging

    # TODO Alert 발송
    for eval_point in metric_cpu.eval_point_group_list:
        # TODO eval_history에 결과 등록 필요
        # TODO alert_history에 결과 들록 필요
        if (
            eval_point.get(TCodeMetricEvalResultType.metric_eval_result_seq.name)
            > EvalResultType.OK.value
        ):
            pass


if __name__ == "__main__":
    metric_cpu_flow()
