from datetime import datetime, timedelta

from prefect.variables import Variable


def get_before_days(x_days_before: str) -> datetime:
    dt = datetime.now() - timedelta(days=int(Variable.get(x_days_before)))
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)
