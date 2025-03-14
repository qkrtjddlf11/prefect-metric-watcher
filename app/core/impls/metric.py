# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from datetime import datetime
from typing import List, Tuple

from sqlalchemy import Row, func
from sqlalchemy.orm import Session, scoped_session

from app.core.db.mariadb.prefect_metric_watcher_model import (
    CodeComparisonOperatorType,
    CodeEvaluateTargetType,
    CodeMetricType,
    EvaluateFlow,
)
from app.core.schemas.mariadb.metric import EvaluateFlows
from common_modules.db.mariadb.metric_watcher_base import (
    TAlertHistory,
    TCodeEvalOperatorType,
    TCodeEvalType,
    TCodeMetricEvalResultType,
    TCodeMetricType,
    TMetricEvalHistory,
    TMetricEvalThreshold,
    TOperationServer,
)
from common_modules.define.name import POINT_HOST_NAME, POINT_TIME_NAME


def fetch_evaluate_flows(
    session: scoped_session[Session],
    metric_type_seq: int,
    evaluate_target_type_seq: int,
) -> EvaluateFlows:
    query = (
        session.query(
            EvaluateFlow.evaluate_flow_seq,
            EvaluateFlow.name.label("evaluate_flow_name"),
            CodeMetricType.metric_type_seq,
            CodeMetricType.name.label("metric_type_name"),
            CodeComparisonOperatorType.comparison_operator_type_seq,
            CodeComparisonOperatorType.name.label("comparison_operator_type_name"),
            EvaluateFlow.evaluate_value,
            CodeEvaluateTargetType.evaluate_target_type_seq,
            CodeEvaluateTargetType.name.label("evaluate_target_type_name"),
        )
        .select_from(EvaluateFlow)
        .join(
            CodeMetricType,
            EvaluateFlow.metric_type_seq == CodeMetricType.metric_type_seq,
        )
        .join(
            CodeComparisonOperatorType,
            EvaluateFlow.comparison_operator_type_seq
            == CodeComparisonOperatorType.comparison_operator_type_seq,
        )
        .join(
            CodeEvaluateTargetType,
            EvaluateFlow.evaluate_target_type_seq
            == CodeEvaluateTargetType.evaluate_target_type_seq,
        )
        .filter(EvaluateFlow.metric_type_seq == metric_type_seq)
        .filter(EvaluateFlow.evaluate_target_type_seq == evaluate_target_type_seq)
    )

    print("=============== Query Statement Start ================")
    print(query.statement)
    print("=============== End Query Statement ================")

    return EvaluateFlows(**query.first()._asdict())


def sql_get_operation_server_list(session, operation_server_name: str) -> int:
    result = (
        session.query(TOperationServer.operation_server_seq)
        .select_from(TOperationServer)
        .filter(TOperationServer.name == operation_server_name)
        .one()
    )

    return result.operation_server_seq


def sql_delete_metric_eval_history(session, after_days) -> int:
    deleted_rows = (
        session.query(TMetricEvalHistory)
        .filter(TMetricEvalHistory.timestamp < after_days)
        .delete()
    )

    session.commit()

    return deleted_rows


def sql_insert_metric_eval_history(
    mariadb_connection,
    session,
    metric_eval_threshold_seq: int,
    eval_point: dict,
    key: str,
) -> None:
    new_entry = TMetricEvalHistory(
        metric_eval_threshold_seq=metric_eval_threshold_seq,
        metric_eval_result_seq=eval_point[
            TCodeMetricEvalResultType.metric_eval_result_seq.name
        ],
        operation_server_seq=mariadb_connection.execute_session_query(
            sql_get_operation_server_list, eval_point.get(POINT_HOST_NAME)
        ),
        metric_eval_result_value=eval_point.get(key),
        timestamp=datetime.strptime(eval_point[POINT_TIME_NAME], "%Y-%m-%dT%H:%M:%SZ"),
    )

    session.add(new_entry)
    session.commit()


def sql_insert_alert_history(
    session, generated_messages: str, alert_send_result: str
) -> None:
    # TODO Alert 보내기가 실패일 경우 Update 하는 스케쥴러 필요.
    send_datetime = None

    if alert_send_result == "Y":
        send_datetime = func.current_timestamp()

    new_entry = TAlertHistory(
        alert_content=generated_messages,
        alert_send_status=alert_send_result,
        send_datetime=send_datetime,
    )

    session.add(new_entry)
    session.commit()
