"""A set of helper functions used internally"""
from typing import Dict
import logging
from datetime import datetime
import re


TIMEOUT=10
HEADERS = {"Content-type": "application/json; charset=UTF-8"}

_LOGGER: logging.Logger = logging.getLogger(__package__)

def auth_headers(access_token: str) -> Dict[str, str]:
    """Given an access token, return the headers we should send to pod point."""
    auth_header = {"Authorization": f"Bearer {access_token}"}
    combined_headers = HEADERS.copy()
    combined_headers.update(auth_header)
    return combined_headers

def lazy_convert_to_datetime(date_string: str) -> datetime:
    """Convert a string datetime representation to a time-zoned datetime object."""
    if date_string is None or not isinstance(date_string, str):
        return None

    # Convert a 'Z' ending string to +00:00 for correct support
    date_string = re.sub(r"Z$", "+00:00", date_string)

    date_time = None
    # Example: 2022-01-25T09:00:00+00:00
    try:
        date_time = datetime.fromisoformat(date_string)
    except ValueError as error:
        _LOGGER.warning("Tried to convert '%s' to datetime but got: %s", date_string, error)

    return date_time

def lazy_iso_format_datetime(date_time: datetime) -> str:
    """Format a datetime object into an iso_format, if a datetime is passed."""
    if not isinstance(date_time, datetime):
        return None

    return date_time.isoformat()
