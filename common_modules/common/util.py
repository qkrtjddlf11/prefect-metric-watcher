# pylint: disable=C0114, C0116, C0115
# coding: utf-8
import datetime
import logging

import pendulum
import pytz
from pytz import UnknownTimeZoneError, timezone


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
