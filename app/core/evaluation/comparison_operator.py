# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from abc import ABC, abstractmethod

from app.core.define.code import ComparisonOperatorType


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
    ComparisonOperatorType.LT.value: LessThan(),
    ComparisonOperatorType.LTE.value: LessThanOrEqual(),
    ComparisonOperatorType.GT.value: GreaterThan(),
    ComparisonOperatorType.GTE.value: GreaterThanOrEqual(),
}
