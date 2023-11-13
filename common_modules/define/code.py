# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from enum import Enum


class MetricType(Enum):
    CPU = 1
    MEMORY = 2
    DISK_ROOT = 3
    DISK_USER_SERVICE = 4
    DISK_STG = 5
    DISK_INODES_ROOT = 6
    DISK_INODES_USER_SERVICE = 7
    DISK_INODES_STG = 8
    DISKIO = 9
    SWAP = 10
    SYSTEM_LOAD5 = 11
    NETSTAT_TCP_ESTABLISHED = 12


class EvalType(Enum):
    XXX = 1
    YYY = 2
    COMMON = 3


class MethodOperatorType(Enum):
    LT = 1
    LTE = 2
    GT = 3
    GTE = 4


class EvalResultType(Enum):
    OK = 1
    ALERT = 2
    SNOOZE = 3
