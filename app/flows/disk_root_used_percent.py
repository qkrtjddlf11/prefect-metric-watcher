# pylint: disable=C0114, C0115, C0116
# coding: utf-8

import logging
import os
import sys
from platform import node, platform

from prefect import cache_policies, context, flow, get_run_logger, task
from prefect.runtime import flow_run
from requests import exceptions

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.core.config.yaml import get_yaml_config
from app.core.db.influxdb.connector import InfluxDBConnector
from app.core.db.mariadb.connector import MariaDBConnector
from app.core.define.base import Path
from app.core.define.code import EvaluateResultType, EvaluateTargetType, MetricType
from app.core.define.flows import MetricWatcher
from app.core.define.tasks import DiskRootUsedPercent
from app.core.evaluation.comparison_operator import OperatorMapping
from app.core.schemas.influxdb.metric import DiskRootUsedPercentPoint
from app.core.schemas.mariadb.metric import EvaluateFlows, EvaluateResultHistory
from app.utils.db import get_evaluate_flows, insert_evaluate_result_history
from app.utils.time import create_basetime, get_run_datetime
from app.utils.webhook import flow_failure_webhook

# Lazy Query 수행 (1분 이내로 데이터 입수가 가능하지 않을 수도 있으므로)
GET_DISK_ROOT_USED_PERCENT_QUERY = """
    SELECT time, server_id, node_id, used_percent
    FROM disk 
    WHERE time > now() - 2m AND time <= now() - 1m
          AND path = '/'
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


@task(
    name=DiskRootUsedPercent.Tasks.COMPARE_DISK_ROOT_USED_PERCENT_NAME,
    task_run_name=f"{DiskRootUsedPercent.Tasks.COMPARE_DISK_ROOT_USED_PERCENT_NAME}_{get_run_datetime()}",
    retries=3,
    retry_delay_seconds=5,
    cache_policy=cache_policies.NO_CACHE,
    description="Compare disk root partition used percent",
)
def compare_disk_root_used_percent(
    evaluate_flow: EvaluateFlows,
    used_percent_points: list[DiskRootUsedPercentPoint],
) -> list[EvaluateResultHistory]:
    evaluate_result_histories = [
        EvaluateResultHistory(
            evaluate_flow_seq=evaluate_flow.evaluate_flow_seq,
            evaluate_result_type_seq=EvaluateResultType.CRITICAL.value,
            result_value=round(point.used_percent, 2),
            node_id=point.node_id,
            server_id=point.server_id,
        )
        for point in used_percent_points
        if OperatorMapping.get(evaluate_flow.comparison_operator_type_seq).compare(
            point.used_percent, evaluate_flow.evaluate_value
        )
    ]

    return evaluate_result_histories


@task(
    name=DiskRootUsedPercent.Tasks.GET_DISK_ROOT_POINTS_NAME,
    task_run_name=f"{DiskRootUsedPercent.Tasks.GET_DISK_ROOT_POINTS_NAME}_{get_run_datetime()}",
    retries=3,
    retry_delay_seconds=5,
    description="Get disk root metric from InfluxDB",
)
def get_disk_root_points(
    logger: logging.Logger, influxdb_connector: InfluxDBConnector
) -> list[DiskRootUsedPercentPoint]:
    with influxdb_connector.get_resource() as conn:
        try:
            results = conn.query(GET_DISK_ROOT_USED_PERCENT_QUERY)
            return [DiskRootUsedPercentPoint(**point) for point in results.get_points()]
        except exceptions.ConnectionError as err:
            logger.error("Connection Error : %s", str(err))
            raise


@flow(
    name=MetricWatcher.Flows.DISK_ROOT_USED_PERCENT_FLOW_NAME,
    flow_run_name=generate_flow_run_name,
    retries=3,
    retry_delay_seconds=5,
    description="Prefect agent module for disk root partition usage",
    timeout_seconds=5,
    on_failure=[flow_failure_webhook],
)
def disk_root_used_percent_flow() -> None:
    logger = get_run_logger()

    logger.info("Network: %s. ✅", node())
    logger.info("Instance: %s. ✅", platform())

    yaml_config = get_yaml_config(logger, Path.CONFIG_PATH)

    mariadb_connector = MariaDBConnector(logger, **yaml_config.mariadb.model_dump())
    influxdb_connector = InfluxDBConnector(logger, **yaml_config.influxdb.model_dump())

    used_percent_points = get_disk_root_points.submit(
        logger, influxdb_connector
    ).result()

    logger.info("used_percent_points: %s. ✅", used_percent_points)

    evaluate_flow = get_evaluate_flows(
        mariadb_connector,
        MetricType.DISK_ROOT_USED_PERCENT.value,
        EvaluateTargetType.COMMON.value,
    )

    logger.info("evaluate_flow: %s. ✅", evaluate_flow)

    evaluate_result_histories = compare_disk_root_used_percent.submit(
        evaluate_flow, used_percent_points
    ).result()

    logger.info("evaluate_result_histories: %s. ✅", evaluate_result_histories)

    insert_evaluate_result_history(mariadb_connector, evaluate_result_histories)


if __name__ == "__main__":
    disk_root_used_percent_flow()
