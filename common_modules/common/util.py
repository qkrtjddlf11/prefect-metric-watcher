# pylint: disable=C0114, C0116, C0115
# coding: utf-8
import datetime
import logging
import os
import sys

import pendulum
import pytz
from prefect import variables
from pytz import UnknownTimeZoneError, timezone

from common_modules.common.base_impl import Metric

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def get_after_days(after_days: str) -> datetime:
    """Get after_days variable from Prefect API

    Returns:
        _type_: datetime
    """

    date = datetime.datetime.now() - datetime.timedelta(
        days=int(variables.get(after_days))
    )

    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def create_basetime(logger: logging, flow_run_timestamp: pendulum.datetime) -> datetime:
    # Cron은 정확하게 14:00:00 시간에 동작하는게 아니므로 시간 보정
    try:
        base_time = (
            datetime.datetime.fromisoformat(flow_run_timestamp.to_datetime_string())
            .astimezone()
            .replace(tzinfo=timezone("UTC"))
        )

        base_time = base_time + datetime.timedelta(seconds=15)
        base_time = base_time.astimezone(pytz.timezone("Asia/Seoul"))
    except UnknownTimeZoneError as err:
        logger.error(err)

    return base_time.replace(second=0, microsecond=0)


def update_point(
    point: dict,
    metric: Metric,
    metric_eval_result_seq_name: str,
    metric_eval_result_seq: int,
) -> None:
    if point is not None:
        point.update({metric_eval_result_seq_name: metric_eval_result_seq})

    metric.eval_point_group_list.append(point)
