import logging

from app.core.config.yaml import YamlConfig
from app.core.db.influxdb.connector import InfluxDBConnector
from app.core.db.mariadb.connector import MariaDBConnector
from app.core.impls.metric import (
    sql_fetch_evaluate_flows,
    sql_insert_evaluate_result_history,
)
from app.core.schemas.mariadb.metric import EvaluateFlows, EvaluateResultHistory


def get_connectors(
    logger: logging.Logger, yaml_config: YamlConfig
) -> tuple[MariaDBConnector, InfluxDBConnector]:
    mariadb_connector = MariaDBConnector(logger, **yaml_config.mariadb.model_dump())
    influxdb_connector = InfluxDBConnector(logger, **yaml_config.influxdb.model_dump())
    return mariadb_connector, influxdb_connector


def get_evaluate_flows(
    mariadb_connector: MariaDBConnector,
    metric_type_value: int,
    evaluate_target_type_value: int,
) -> EvaluateFlows:
    evaluate_flow: EvaluateFlows = mariadb_connector.execute_session_query(
        sql_fetch_evaluate_flows, metric_type_value, evaluate_target_type_value
    )
    return evaluate_flow


def insert_evaluate_result_history(
    mariadb_connector: MariaDBConnector,
    evaluate_result_histories: list[EvaluateResultHistory],
) -> None:
    mariadb_connector.execute_session_query(
        sql_insert_evaluate_result_history, evaluate_result_histories
    )
