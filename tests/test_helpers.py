from re import X
from datetime import datetime, timezone, timedelta
import pytest
import pytz
from podpointclient.helpers.helpers import Helpers
import logging

def test_auth_headers():
    expected = {"Content-type": "application/json; charset=UTF-8", "Authorization": "Bearer 1234"}

    helpers = Helpers()
    assert helpers.auth_headers("1234") == expected

def test_lazy_convert_to_datetime(caplog):
    helpers = Helpers()

    # Correct type but wrong content
    caplog.set_level(logging.WARNING)
    caplog.clear()
    assert helpers.lazy_convert_to_datetime("Break Me") is None
    assert caplog.record_tuples == [("podpointclient.helpers", logging.WARNING, "Tried to convert 'Break Me' to datetime but got: Invalid isoformat string: 'Break Me'")]

    # Unsupported data types
    assert helpers.lazy_convert_to_datetime(None) is None
    assert helpers.lazy_convert_to_datetime(1) is None
    assert helpers.lazy_convert_to_datetime(False) is None
    assert helpers.lazy_convert_to_datetime({}) is None

    ams = pytz.timezone("Europe/Amsterdam")

    # Successful conversions
    assert helpers.lazy_convert_to_datetime("2022-01-25T09:00:00+00:00:00") == datetime(2022,1,25,9,0,0, tzinfo=timezone.utc)
    assert helpers.lazy_convert_to_datetime("2022-01-25T09:00:00+01:00:00") == ams.localize(datetime(2022,1,25,9,0,0))
    assert helpers.lazy_convert_to_datetime("2022-01-25T09:00:00Z") == datetime(2022,1,25,9,0,0, tzinfo=timezone.utc)