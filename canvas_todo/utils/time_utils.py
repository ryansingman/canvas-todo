from datetime import datetime, timezone
from dateutil import tz


DUE_DATE_FORMAT = "%m/%d/%Y @ %I:%M%p"
ISO8601_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def gen_due_date_str(date_str: str) -> str:
    """Converts ISO8601 string to formatted due date string

    Parameters
    ----------
    date_str : str
        ISO8601 date string

    Returns
    -------
    str
        formatted due date string
    """
    return from_iso8601(date_str).strftime(DUE_DATE_FORMAT)


def from_due_date_str(date_str: str) -> datetime:
    """Converts formatted due date string to datetime object

    Parameters
    ----------
    date_str : str
        formatted datetime string

    Returns
    -------
    datetime
        datetime object, created from date string
    """
    return datetime.strptime(
        date_str, DUE_DATE_FORMAT
    ).astimezone(tz.tzlocal()).replace(second=0)


def to_due_date_str(dt: datetime) -> str:
    """Converts from datetime object to due date string

    Parameters
    ----------
    dt : datetime
        datetime object to convert

    Returns
    -------
    str
        formatted due date string
    """
    return dt.strftime(DUE_DATE_FORMAT)


def from_iso8601(date_str: str) -> datetime:
    """Converts ISO8601 string to datetime object in local timezone

    Parameters
    ----------
    date_str : str
        ISO8601 date string

    Returns
    -------
    datetime
        datetime object, created from date str
    """
    return datetime.strptime(
        date_str, ISO8601_DATE_FORMAT
    ).replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()).replace(second=0)
