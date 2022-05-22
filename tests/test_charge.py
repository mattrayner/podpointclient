import json
from podpointclient.charge import Charge, ChargeDurationFormat
from datetime import datetime, timezone

def test_charge():
    charges_data = json.load(open('./tests/fixtures/complete_charges.json')).get('charges', [])
    ongoing_charge_data = charges_data[0]
    completed_charge_data = charges_data[1]

    ongoing_charge = Charge(data=ongoing_charge_data)
    assert 1 == ongoing_charge.id
    assert 12.2 == ongoing_charge.kwh_used
    assert 0 == ongoing_charge.duration
    assert datetime(
        year=2022,
        month=5,
        day=22,
        hour=17,
        minute=23,
        second=14,
        tzinfo=timezone.utc
    ) == ongoing_charge.starts_at
    assert None == ongoing_charge.ends_at

    assert None == ongoing_charge.charging_duration.raw
    assert [] == ongoing_charge.charging_duration.formatted
    assert "" == str(ongoing_charge.charging_duration)

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
    assert 2.8 == completed_charge.kwh_used
    assert 1444 == completed_charge.duration
    assert datetime(
        year=2022,
        month=5,
        day=21,
        hour=10,
        minute=57,
        second=34,
        tzinfo=timezone.utc
    ) == completed_charge.starts_at
    assert datetime(
        year=2022,
        month=5,
        day=22,
        hour=11,
        minute=2,
        second=28,
        tzinfo=timezone.utc
    ) == completed_charge.ends_at

    assert 2492 == completed_charge.charging_duration.raw
    assert [ChargeDurationFormat(value = '41', unit='minutes')] == completed_charge.charging_duration.formatted
    assert "41 minutes" == str(completed_charge.charging_duration)

    completed_charge.charging_duration.formatted = [ChargeDurationFormat(value = '2', unit='hours'), ChargeDurationFormat(value = '41', unit='minutes')]
    assert "2 hours 41 minutes" == str(completed_charge.charging_duration)

    assert 1234 == completed_charge.location.id
    assert True == completed_charge.location.home

    assert 1234 == completed_charge.location.address.id
    assert "" == completed_charge.location.address.business_name

    assert "Europe/London" == completed_charge.location.timezone

    assert 198765 == completed_charge.pod.id

    assert 51 == completed_charge.energy_cost

    assert None == completed_charge.organisation.id
    assert None == completed_charge.organisation.name
    assert True == completed_charge.home