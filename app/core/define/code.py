from enum import Enum


class AlertType(Enum):
    GMAIL = 1
    SLACK = 2


class ComparisonOperatorType(Enum):
    LT = 1
    LTE = 2
    GT = 3
    GTE = 4
    EQ = 5
    NE = 6
    RE = 7


class EvaluateResultType(Enum):
    OK = 1
    WARNING = 2
    CRITICAL = 3
    EMPTY = 4


class EvaluateTargetType(Enum):
    COMMON = 1
    NODE = 2
    SERVER = 3


class MetricType(Enum):
    CPU_USED_PERCENT: 1
    MEMORY_USED_PERCENT: 2
    DISK_USED_PERCENT_ROOT: 3
