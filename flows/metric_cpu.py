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

BASE_CONFIG_PATH = "config/config_dev.yaml"

query = """SELECT time, host, (100 - usage_idle) as usage_percent FROM cpu WHERE cpu = 'cpu-total' AND time > now() - 1m TZ('Asia/Seoul')"""


def metric_cpu_flow():
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

    # TODO InfluxDB 조회 및 평가
    with influx.get_resource() as conn:
        try:
            results = conn.query(query)
        except exceptions.ConnectionError as err:
            logger.error("Connection Error : %s", str(err))
            sys.exit(1)

        for point in results.get_points():
            print(point)

    # TODO Individual 임계치 조회 및 평가
    logger.info("Compare data")

    # TODO Alert 발송
    logger.info("Alert Send!")


if __name__ == "__main__":
    metric_cpu_flow()
