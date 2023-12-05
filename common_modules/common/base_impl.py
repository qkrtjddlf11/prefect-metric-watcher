# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from typing import List, Tuple

from sqlalchemy import Row

from common_modules.db.mariadb.metric_watcher_base import (
    TCodeEvalOperatorType,
    TCodeEvalType,
    TCodeMetricType,
    TMetricEvalHistory,
    TMetricEvalThreshold,
    TOperationServer,
)


class Metric:
    def __init__(
        self,
        metric_eval_threshold_seq: int = 0,
        metric_type_seq: int = 0,
        metric_type_name: str = "",
        eval_type_seq: int = 0,
        eval_type_name: str = "",
        operation_server_seq: int = 0,
        operation_server_name: str = "",
        eval_value: int = 0,
        eval_operator_type_seq: int = 0,
        operator_name: str = "",
    ) -> None:
        self.metric_eval_threshold_seq = metric_eval_threshold_seq
        self.metric_type_seq = metric_type_seq
        self.metric_type_name = metric_type_name
        self.eval_type_seq = eval_type_seq
        self.eval_type_name = eval_type_name
        self.operation_server_seq = operation_server_seq
        self.operation_server_name = operation_server_name
        self.eval_value = eval_value
        self.eval_operator_type_seq = eval_operator_type_seq
        self.operator_name = operator_name
        self.eval_point_group_list = []

    def __str__(self) -> str:
        return (
            f"Metric(metric_eval_threshold_seq={self.metric_eval_threshold_seq}, "
            + f"metric_type_seq={self.metric_type_seq}, "
            + f"metric_type_name={self.metric_type_name}, "
            + f"eval_type_seq={self.eval_type_seq}, "
            + f"eval_type_name={self.eval_type_name}, "
            + f"operation_server_seq={self.operation_server_seq}, "
            + f"operation_server_name={self.operation_server_name}, "
            + f"eval_value={self.eval_value}, "
            + f"eval_operator_type_seq={self.eval_operator_type_seq}, "
            + f"operator_name={self.operator_name}, "
            + f"eval_point_group_list={self.eval_point_group_list}"
        )


def sql_get_metric_eval_threshold_list(
    session, metric_type_seq: int, eval_type_seq: int
) -> List[Row[Tuple[int, str, int, int, str]]]:
    query = (
        session.query(
            TMetricEvalThreshold.metric_eval_threshold_seq,
            TMetricEvalThreshold.metric_type_seq,
            TCodeMetricType.name,
            TCodeEvalType.eval_type_seq,
            TCodeEvalType.name,
            TMetricEvalThreshold.operation_server_seq,
            TOperationServer.name,
            TMetricEvalThreshold.eval_value,
            TMetricEvalThreshold.eval_operator_type_seq,
            TCodeEvalOperatorType.name,
        )
        .select_from(TMetricEvalThreshold)
        .join(
            TCodeEvalType,
            TMetricEvalThreshold.eval_type_seq == TCodeEvalType.eval_type_seq,
        )
        .join(
            TCodeMetricType,
            TMetricEvalThreshold.metric_type_seq == TCodeMetricType.metric_type_seq,
        )
        .join(
            TCodeEvalOperatorType,
            TMetricEvalThreshold.eval_operator_type_seq
            == TCodeEvalOperatorType.eval_operator_type_seq,
        )
        .join(
            TOperationServer,
            TMetricEvalThreshold.operation_server_seq
            == TOperationServer.operation_server_seq,
        )
        .filter(TMetricEvalThreshold.metric_type_seq == metric_type_seq)
        .filter(TMetricEvalThreshold.eval_type_seq == eval_type_seq)
    )

    print("=============== Query Statement Start ================")
    print(query.statement)
    print("=============== End Query Statement ================")

    return query.all()


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
