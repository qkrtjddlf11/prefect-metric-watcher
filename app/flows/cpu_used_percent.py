# pylint: disable=C0114, C0115, C0116
# coding: utf-8


import logging
import os
import sys
from platform import node, platform

from prefect import cache_policies, context, flow, get_run_logger, task
from prefect.runtime import flow_run
from requests import exceptions
from yaml import YAMLError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.config.yaml import YamlConfig
from app.core.db.influxdb.connector import InfluxDBConnector
from app.core.define.base import Path
from app.core.define.code import EvaluateResultType
from app.core.define.flows import MetricWatcher
from app.core.define.tasks import CpuUsedPercent
from app.core.evaluation.comparison_operator import OperatorMapping
from app.core.schemas.influxdb.metric import UsedPercentPoint
from app.core.schemas.mariadb.metric import EvaluateFlows, EvaluateResultHistory
from app.utils.db import get_connectors, get_evaluate_flows
from app.utils.time import create_basetime, get_run_datetime

# Lazy Query 수행 (1분 이내로 데이터 입수가 가능하지 않을 수도 있으므로)
GET_CPU_USAGE_PERCENT_QUERY = """
    SELECT time, server_id, node_id, (100 - usage_idle) as usage_percent
    FROM cpu 
    WHERE time > now() - 2m AND time <= now() - 1m
    GROUP BY host limit 1
"""


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


def update_evaluate_result_history():
    pass


@task(
    name=CpuUsedPercent.Tasks.COMPARE_CPU_USED_PERCENT_NAME,
    task_run_name=f"{CpuUsedPercent.Tasks.COMPARE_CPU_USED_PERCENT_NAME}_{get_run_datetime()}",
    retries=3,
    retry_delay_seconds=5,
    cache_policy=cache_policies.NO_CACHE,
    description="Compare cpu used percent",
)
def compare_cpu_used_percent(
    evaluate_flow: EvaluateFlows,
    used_percent_points: list[UsedPercentPoint],
) -> list[EvaluateResultHistory]:
    evaluate_result_histories = [
        EvaluateResultHistory(
            evaluate_flow_seq=evaluate_flow.evaluate_flow_seq,
            evaluate_result_type_seq=EvaluateResultType.CRITICAL.value,
            node_id=point.node_id,
            server_id=point.server_id,
        )
        for point in used_percent_points
        if OperatorMapping.get(evaluate_flow.comparison_operator_type_seq).compare(
            point.usage_percent, evaluate_flow.evaluate_value
        )
    ]

    return evaluate_result_histories


@task(
    name=CpuUsedPercent.Tasks.GET_CPU_POINTS_NAME,
    task_run_name=f"{CpuUsedPercent.Tasks.GET_CPU_POINTS_NAME}_{get_run_datetime()}",
    retries=3,
    retry_delay_seconds=5,
    description="Get CPU metric from InfluxDB",
)
def get_cpu_points(
    logger: logging.Logger, influxdb_connector: InfluxDBConnector
) -> list[UsedPercentPoint]:
    with influxdb_connector.get_resource() as conn:
        try:
            results = conn.query(GET_CPU_USAGE_PERCENT_QUERY)
            return [UsedPercentPoint(**point) for point in results.get_points()]
        except exceptions.ConnectionError as err:
            logger.error("Connection Error : %s", str(err))
            raise


@flow(
    name=MetricWatcher.Flows.CPU_USED_PERCENT_FLOW_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="Prefect agent module for CPU usage",
    timeout_seconds=5,
    # on_failure=[flow_failure_webhook],
)
def cpu_used_percent_flow() -> None:
    logger = get_run_logger()

    logger.info("Network: %s. ✅", node())
    logger.info("Instance: %s. ✅", platform())

    try:
        yaml_config = YamlConfig.load_yaml(base_path=Path.CONFIG_PATH, mode="dev")
    except FileNotFoundError as err:
        logger.error("File Not Found : %s", str(err))
        raise
    except YAMLError as err:
        logger.error("Yaml load Error : %s", str(err))
        raise

    mariadb_connector, influxdb_connector = get_connectors(logger, yaml_config)

    used_percent_points = get_cpu_points.submit(logger, influxdb_connector).result()

    evaluate_flow = get_evaluate_flows(mariadb_connector)
    evaluate_result_histories = compare_cpu_used_percent.submit(
        evaluate_flow, used_percent_points
    ).result()

    for history in evaluate_result_histories:
        print(history)


if __name__ == "__main__":
    cpu_used_percent_flow()
