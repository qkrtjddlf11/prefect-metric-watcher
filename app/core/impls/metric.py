# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from datetime import datetime

from sqlalchemy.orm import Session, scoped_session

from app.core.db.mariadb.prefect_metric_watcher_model import (
    TCodeComparisonOperatorType,
    TCodeEvaluateTargetType,
    TCodeMetricType,
    TEvaluateFlow,
    TEvaluateResultHistory,
)
from app.core.schemas.mariadb.metric import EvaluateFlows, EvaluateResultHistory


def sql_fetch_evaluate_flows(
    session: scoped_session[Session],
    metric_type_seq: int,
    evaluate_target_type_seq: int,
) -> EvaluateFlows:
    query = (
        session.query(
            TEvaluateFlow.evaluate_flow_seq,
            TEvaluateFlow.name.label("evaluate_flow_name"),
            TCodeMetricType.metric_type_seq,
            TCodeMetricType.name.label("metric_type_name"),
            TCodeComparisonOperatorType.comparison_operator_type_seq,
            TCodeComparisonOperatorType.name.label("comparison_operator_type_name"),
            TEvaluateFlow.evaluate_value,
            TCodeEvaluateTargetType.evaluate_target_type_seq,
            TCodeEvaluateTargetType.name.label("evaluate_target_type_name"),
        )
        .select_from(TEvaluateFlow)
        .join(
            TCodeMetricType,
            TEvaluateFlow.metric_type_seq == TCodeMetricType.metric_type_seq,
        )
        .join(
            TCodeComparisonOperatorType,
            TEvaluateFlow.comparison_operator_type_seq
            == TCodeComparisonOperatorType.comparison_operator_type_seq,
        )
        .join(
            TCodeEvaluateTargetType,
            TEvaluateFlow.evaluate_target_type_seq
            == TCodeEvaluateTargetType.evaluate_target_type_seq,
        )
        .filter(TEvaluateFlow.metric_type_seq == metric_type_seq)
        .filter(TEvaluateFlow.evaluate_target_type_seq == evaluate_target_type_seq)
    )

    print("=============== Query Statement Start ================")
    print(query.statement)
    print("=============== End Query Statement ================")

    return EvaluateFlows(**query.first()._asdict())


def sql_insert_evaluate_result_history(
    session: scoped_session[Session],
    evaluate_result_histories: list[EvaluateResultHistory],
) -> None:
    session.bulk_insert_mappings(TEvaluateResultHistory, evaluate_result_histories)
    session.commit()


def sql_delete_evaluate_result_history(
    session: scoped_session[Session], x_days_before: datetime
) -> int:
    deleted_rows = (
        session.query(TEvaluateResultHistory)
        .filter(TEvaluateResultHistory.timestamp < x_days_before)
        .delete()
    )
    session.commit()
    return deleted_rows
