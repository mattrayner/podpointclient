import json
from freezegun import freeze_time
from podpointclient.charge_override import ChargeOverride
from datetime import datetime, timezone, timedelta

@freeze_time("Jan 1st, 2022")
def test_complete_charge_override():
    charge_override_data = {
        "ppid": "PSL-123456",
        "requested_at": "2022-01-01T00:00:00.000Z",
        "received_at": "2022-01-01T00:00:00.000Z",
        "ends_at": "2022-01-01T03:02:01.000Z"
    }
    charge_override = ChargeOverride(data=charge_override_data)

    assert charge_override.ppid == 'PSL-123456'
    assert charge_override.requested_at == datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc) 
    assert charge_override.received_at == datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc) 
    assert charge_override.ends_at == datetime(2022, 1, 1, 3, 2, 1, tzinfo=timezone.utc) 

    assert charge_override.dict == {
        "ppid": "PSL-123456",
        "requested_at": "2022-01-01T00:00:00+00:00",
        "received_at": "2022-01-01T00:00:00+00:00",
        "ends_at": "2022-01-01T03:02:01+00:00"
    }

    # Test active
    assert charge_override.active is True
    assert charge_override.remaining_time == timedelta(hours=3, minutes=2, seconds=1)
    
    charge_override.ends_at = datetime(2021, 1, 1, 3, 2, 1, tzinfo=timezone.utc) 
    assert charge_override.active is False
    assert charge_override.remaining_time is None
    
    charge_override.ends_at = None
    assert charge_override.active is False
    assert charge_override.remaining_time is None

def test_empty_charge_override():
    charge_override = ChargeOverride(data={})

    assert charge_override.ppid is None
    assert charge_override.requested_at is None
    assert charge_override.received_at is None
    assert charge_override.ends_at is None

    assert charge_override.dict == {
        "ppid": None,
        "requested_at": None,
        "received_at": None,
        "ends_at": None
    }

    assert charge_override.active is False
