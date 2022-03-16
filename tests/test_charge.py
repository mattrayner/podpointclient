import json
from podpointclient.charge import Charge
from datetime import datetime, timezone

def test_charge():
    charges_data = json.load(open('./tests/fixtures/complete_charges.json')).get('charges', [])
    ongoing_charge_data = charges_data[0]
    completed_charge_data = charges_data[1]

    ongoing_charge = Charge(data=ongoing_charge_data)
    assert 1 == ongoing_charge.id
    assert 3.2 == ongoing_charge.kwh_used
    assert 0 == ongoing_charge.duration
    assert datetime(
        year=2022,
        month=3,
        day=8,
        hour=0,
        minute=0,
        second=0,
        tzinfo=timezone.utc
    ) == ongoing_charge.starts_at
    assert None == ongoing_charge.ends_at

    assert 1234 == ongoing_charge.location.id
    assert True == ongoing_charge.location.home

    assert 1234 == ongoing_charge.location.address.id
    assert "" == ongoing_charge.location.address.business_name

    assert "Europe/London" == ongoing_charge.location.timezone

    assert 198765 == ongoing_charge.pod.id

    assert 0 == ongoing_charge.energy_cost

    assert None == ongoing_charge.organisation.id
    assert None == ongoing_charge.organisation.name
    assert True == ongoing_charge.home

    completed_charge = Charge(data=completed_charge_data)
    assert 2 == completed_charge.id
    assert 6.3 == completed_charge.kwh_used
    assert 1393 == completed_charge.duration
    assert datetime(
        year=2022,
        month=3,
        day=10,
        hour=13,
        minute=0,
        second=0,
        tzinfo=timezone.utc
    ) == completed_charge.starts_at
    assert datetime(
        year=2022,
        month=3,
        day=11,
        hour=12,
        minute=0,
        second=0,
        tzinfo=timezone.utc
    ) == completed_charge.ends_at

    assert 1234 == completed_charge.location.id
    assert True == completed_charge.location.home

    assert 1234 == completed_charge.location.address.id
    assert "" == completed_charge.location.address.business_name

    assert "Europe/London" == completed_charge.location.timezone

    assert 198765 == completed_charge.pod.id

    assert 116 == completed_charge.energy_cost

    assert None == completed_charge.organisation.id
    assert None == completed_charge.organisation.name
    assert True == completed_charge.home