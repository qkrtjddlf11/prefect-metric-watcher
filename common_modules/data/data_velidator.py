# pylint: disable=C0114, C0115, C0116
# coding: utf-8

import logging
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from common_modules.common.base_impl import Metric
from common_modules.define.code import (
    E_INVALID_EVAL_TYPE_SEQ,
    E_INVALID_METHOD_OPERATOR_TYPE_SEQ,
    E_INVALID_METRIC_TYPE_SEQ,
    E_INVALID_NONE_DATA,
    EvalType,
    MethodOperatorType,
    MetricType,
)


def verify_data(logger: logging.Logger, metric: Metric) -> bool:
    logger.info("Metric : %s", metric)

    if metric is None:
        logger.error(E_INVALID_NONE_DATA)
        return False

    if metric.metric_type_seq not in (member.value for member in MetricType):
        logger.error(E_INVALID_METRIC_TYPE_SEQ + " :", metric.metric_type_seq)
        return False

    if metric.eval_type_seq not in (member.value for member in EvalType):
        logger.error(E_INVALID_EVAL_TYPE_SEQ + " :", metric.eval_type_seq)
        return False

    if metric.eval_operator_type_seq not in (
        member.value for member in MethodOperatorType
    ):
        logger.error(
            E_INVALID_METHOD_OPERATOR_TYPE_SEQ + " :", metric.eval_operator_type_seq
        )
        return False

    return True
