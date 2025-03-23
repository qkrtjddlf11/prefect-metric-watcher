# pylint: disable=C0114, C0115, C0116
# coding: utf-8

from datetime import datetime, timedelta

from prefect.variables import Variable


def get_before_days(x_days_before: str) -> datetime:
    dt = datetime.now() - timedelta(days=int(Variable.get(x_days_before)))
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
