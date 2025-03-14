import logging
from datetime import datetime, timedelta

import pendulum
import pytz
from pytz import UnknownTimeZoneError, timezone


def create_basetime(logger: logging, flow_run_timestamp: pendulum.DateTime) -> datetime:
    try:
        base_time = (
            datetime.fromisoformat(flow_run_timestamp.to_datetime_string())
            .astimezone()
            .replace(tzinfo=timezone("UTC"))
        )

        base_time = base_time + timedelta(seconds=15)
        base_time = base_time.astimezone()
    except UnknownTimeZoneError as err:
        logger.error(err)

    return base_time.replace(second=0, microsecond=0)


def get_run_datetime() -> str:
    return datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y%m%d%H%M%S")
