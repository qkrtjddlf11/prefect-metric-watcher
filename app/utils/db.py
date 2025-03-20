from app.core.db.mariadb.connector import MariaDBConnector
from app.core.impls.metric import (
    sql_fetch_evaluate_flows,
    sql_insert_evaluate_result_history,
)
from app.core.schemas.mariadb.metric import EvaluateFlows, EvaluateResultHistory


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
