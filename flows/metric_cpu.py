# pylint: disable=C0114, C0115, C0116
# coding: utf-8


import logging
import os
import sys
from platform import node, platform

from requests import exceptions
from yaml import YAMLError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.config.yaml_config import YamlConfig
from common_modules.db.influxdb.conn import InfluxDBConnection
from common_modules.db.mariadb.conn import MariaDBConnection
from common_modules.db.mariadb.metric_watcher_base import TMetricThreshold, TMetricType
from common_modules.define.metric import MetricType

BASE_CONFIG_PATH = "config/config_dev.yaml"
CPU_USAGE_PERCENT = "usage_percent"

# Lazy Query 수행 (1분 이내로 데이터 입수가 가능하지 않을 수도 있으므로)
CPU_QUERY = """SELECT time, host, (100 - usage_idle) as usage_percent FROM cpu WHERE time > now() - 2m AND time <= now() - 1m  GROUP BY host"""


def metric_cpu_flow(metric_type_seq: int):
    logger = logging.getLogger("")

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

    influx = InfluxDBConnection(logger, *yaml_config.get_all_config().get("INFLUXDB").values())

    # TODO InfluxDB 데이터 조회
    with influx.get_resource() as conn:
        try:
            results = conn.query(CPU_QUERY)
        except exceptions.ConnectionError as err:
            logger.error("Connection Error : %s", str(err))
            sys.exit(1)

        metric_points = results.get_points()

    for point in metric_points:
        print(point)

    # TODO MariaDB 조회 및 InfluxDB 데이터 평가
    mariadb_connection = MariaDBConnection(
        logger, *yaml_config.get_all_config().get("MARIADB").values()
    )

    with mariadb_connection.get_resources() as session:
        query = (
            session.query(TMetricThreshold.metric_threshold_seq, TMetricThreshold.threshold_value)
            .select_from(TMetricThreshold)
            .join(TMetricType, TMetricThreshold.metric_threshold_seq == TMetricType.metric_seq)
            .filter(TMetricThreshold.metric_threshold_seq == metric_type_seq)
        )

        print("=============== Query Statement Start ================")
        print(query.statement)
        print("=============== End Query Statement ================")

    threshold_value = query.all()[0][1]

    for point in metric_points:
        if point.get(CPU_USAGE_PERCENT) > threshold_value:
            print("Alert! ", point)

    # TODO Alert 발송
    logger.info("Alert Send!")


if __name__ == "__main__":
    metric_cpu_flow(MetricType.CPU.value)
