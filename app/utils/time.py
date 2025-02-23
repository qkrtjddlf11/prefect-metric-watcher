import datetime
import logging

import pendulum
import pytz
from pytz import UnknownTimeZoneError, timezone


def create_basetime(logger: logging, flow_run_timestamp: pendulum.DateTime) -> datetime:
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
