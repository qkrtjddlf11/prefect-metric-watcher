from datetime import datetime, timedelta

from prefect.variables import Variable


def get_after_days(after_days: str) -> datetime:
    """Get after_days variable from Prefect API

    Returns:
        _type_: datetime
    """

    date = datetime.now() - timedelta(days=int(Variable.get(after_days)))

    return date.replace(hour=0, minute=0, second=0, microsecond=0)
