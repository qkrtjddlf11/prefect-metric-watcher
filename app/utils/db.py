import logging

from app.core.config.yaml import YamlConfig
from app.core.db.influxdb.connector import InfluxDBConnector
from app.core.db.mariadb.connector import MariaDBConnector
from app.core.define.code import EvaluateTargetType, MetricType
from app.core.impls.metric import fetch_evaluate_flows
from app.core.schemas.mariadb.metric import EvaluateFlows


def get_connectors(
    logger: logging.Logger, yaml_config: YamlConfig
) -> tuple[MariaDBConnector, InfluxDBConnector]:
    mariadb_connector = MariaDBConnector(logger, **yaml_config.mariadb.model_dump())
    influxdb_connector = InfluxDBConnector(logger, **yaml_config.influxdb.model_dump())
    return mariadb_connector, influxdb_connector


def get_evaluate_flows(mariadb_connector: MariaDBConnector) -> EvaluateFlows:
    evaluate_flow: EvaluateFlows = mariadb_connector.execute_session_query(
        fetch_evaluate_flows,
        MetricType.CPU_USED_PERCENT.value,
        EvaluateTargetType.COMMON.value,
    )
    return evaluate_flow
