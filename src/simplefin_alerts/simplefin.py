"""SimpleFin API client."""

from __future__ import annotations

import datetime
import time

import requests


def parse_access_url(access_url: str) -> tuple[str, str, str]:
    """
    Parse SimpleFin access URL into components.

    Args:
        access_url: URL in format scheme://username:password@host/path

    Returns:
        Tuple of (base_url, username, password)
    """
    scheme, rest = access_url.split("//", 1)
    # Split from the right to handle @ in password
    auth, host = rest.rsplit("@", 1)
    base_url = scheme + "//" + host
    username, password = auth.split(":", 1)
    return base_url, username, password


def get_account_errors(
    access_url: str,
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
) -> list:
    """
    Query SimpleFin API for account errors.

    Args:
        access_url: SimpleFin access URL with embedded credentials
        start_date: Start date for query (defaults to yesterday)
        end_date: End date for query (defaults to today)

    Returns:
        List of error strings from SimpleFin
    """
    base_url, username, password = parse_access_url(access_url)
    url = base_url + "/accounts"

    # Default to checking the last day
    if start_date is None:
        start_date = datetime.date.today() - datetime.timedelta(days=1)
    if end_date is None:
        end_date = datetime.date.today()

    start_unixtime = int(round(time.mktime(start_date.timetuple())))
    end_unixtime = int(round(time.mktime(end_date.timetuple())))

    response = requests.get(
        url,
        auth=(username, password),
        params={"start-date": start_unixtime, "end-date": end_unixtime},
    )
    response.raise_for_status()
    data = response.json()

    return data.get("errors", [])
