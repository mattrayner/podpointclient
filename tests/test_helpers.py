from re import X
from datetime import datetime, timezone, timedelta
import pytest
import pytz
from podpointclient.helpers.functions import auth_headers, lazy_convert_to_datetime, lazy_iso_format_datetime
import logging

def test_auth_headers():
    expected = {"Content-type": "application/json; charset=UTF-8", "Authorization": "Bearer 1234"}

    assert auth_headers("1234") == expected

def test_lazy_convert_to_datetime(caplog):
    # Correct type but wrong content
    caplog.set_level(logging.WARNING)
    caplog.clear()
    assert lazy_convert_to_datetime("Break Me") is None
    assert caplog.record_tuples == [("podpointclient.helpers", logging.WARNING, "Tried to convert 'Break Me' to datetime but got: Invalid isoformat string: 'Break Me'")]

    # Unsupported data types
    assert lazy_convert_to_datetime(None) is None
    assert lazy_convert_to_datetime(1) is None
    assert lazy_convert_to_datetime(False) is None
    assert lazy_convert_to_datetime({}) is None

    ams = pytz.timezone("Europe/Amsterdam")

    # Successful conversions
    assert lazy_convert_to_datetime("2022-01-25T09:00:00+00:00:00") == datetime(2022,1,25,9,0,0, tzinfo=timezone.utc)
    assert lazy_convert_to_datetime("2022-01-25T09:00:00+01:00:00") == ams.localize(datetime(2022,1,25,9,0,0))
    assert lazy_convert_to_datetime("2022-01-25T09:00:00Z") == datetime(2022,1,25,9,0,0, tzinfo=timezone.utc)

def test_lazy_iso_format_datetime():
    # When passing a non-datetime
    assert lazy_iso_format_datetime(date_time=12345) == None

    # When passing a datetime
    assert lazy_iso_format_datetime(date_time=datetime(2022,1,25,9,0,0, tzinfo=timezone.utc)) == "2022-01-25T09:00:00+00:00"