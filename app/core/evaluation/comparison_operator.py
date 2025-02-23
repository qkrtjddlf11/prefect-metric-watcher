# pylint: disable=C0114, C0115, C0116
# coding: utf-8
from abc import ABC, abstractmethod

from common_modules.define.code import MethodOperatorType


class ComparisonOperator(ABC):
    @abstractmethod
    def compare(self, target_value, eval_value):
        pass


class GreaterThanOrEqual(ComparisonOperator):
    def compare(self, target_value, eval_value):
        return target_value >= eval_value


class GreaterThan(ComparisonOperator):
    def compare(self, target_value, eval_value):
        return target_value > eval_value


class LessThan(ComparisonOperator):
    def compare(self, target_value, eval_value):
        return target_value < eval_value


class LessThanOrEqual(ComparisonOperator):
    def compare(self, target_value, eval_value):
        return target_value <= eval_value


OperatorMapping = {
    MethodOperatorType.LT.value: LessThan(),
    MethodOperatorType.LTE.value: LessThanOrEqual(),
    MethodOperatorType.GT.value: GreaterThan(),
    MethodOperatorType.GTE.value: GreaterThanOrEqual(),
}
