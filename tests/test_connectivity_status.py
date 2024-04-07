import pytest
from podpointclient.connectivity_status import ConnectivityStatus, Evse
from datetime import datetime, timezone


@pytest.fixture
def connectivity_state_data():
    return {
        "ppid": "PSL-266056",
        "evses": [{
            "id": 1,
            "connectivityState": {
                "protocol": "POW",
                "connectivityStatus": "ONLINE",
                "signalStrength": -68,
                "lastMessageAt": "2024-04-05T18:36:29Z",
                "connectionStartedAt": "2024-04-05T18:26:26.819Z",
                "connectionQuality": 3
            },
            "connectors": [{
                "id": 1,
                "door": "A",
                "chargingState": "SUSPENDED_EV"
            }],
            "architecture": "arch3",
            "energyOfferStatus": {
                "isOfferingEnergy": True,
                "reason": "CHARGE_SCHEDULE",
                "until": None,
                "randomDelay": None,
                "doNotCache": False
            }
        }],
        "connectedComponents": ["evses"]
    }


def test_connectivity_state_initialization(connectivity_state_data):
    cs = ConnectivityStatus(connectivity_state_data)
    assert cs.ppid == "PSL-266056"
    assert cs.connected_components == ["evses"]
    assert len(cs.evses) == 1

    assert Evse == type(cs.evses[0])
    assert cs.evses[0].id == 1
    assert cs.evses[0].connectivity_state.protocol == "POW"
    assert cs.evses[0].connectivity_state.connectivity_status == "ONLINE"
    assert cs.evses[0].connectivity_state.signal_strength == -68
    assert cs.evses[0].connectivity_state.last_message_at == datetime(
        year=2024,
        month=4,
        day=5,
        hour=18,
        minute=36,
        second=29,
        tzinfo=timezone.utc
    )
    assert cs.evses[0].connectivity_state.connection_started_at == datetime(
        year=2024,
        month=4,
        day=5,
        hour=18,
        minute=26,
        second=26,
        microsecond=819000,
        tzinfo=timezone.utc
    )
    assert cs.evses[0].connectivity_state.connection_quality == 3
    assert cs.evses[0].connectors[0].id == 1
    assert cs.evses[0].connectors[0].door == "A"
    assert cs.evses[0].connectors[0].charging_state == "SUSPENDED_EV"
    assert cs.evses[0].architecture == "arch3"

    print(cs.evses[0].energy_offer_status)

    assert cs.evses[0].energy_offer_status.is_offering_energy is True
    assert cs.evses[0].energy_offer_status.reason == "CHARGE_SCHEDULE"
    assert cs.evses[0].energy_offer_status.until is None
    assert cs.evses[0].energy_offer_status.random_delay is None
    assert cs.evses[0].energy_offer_status.do_not_cache is False


def test_connectivity_state_to_json(connectivity_state_data):
    cs = ConnectivityStatus(connectivity_state_data)
    json_data = cs.to_json()
    assert isinstance(json_data, str)


def test_connectivity_status_properties(connectivity_state_data):
    cs = ConnectivityStatus(connectivity_state_data)
    assert cs.connectivity_status == "ONLINE"
    assert cs.last_message_at == datetime(2024, 4, 5, 18, 36, 29, tzinfo=timezone.utc)
    assert cs.charging_state == "SUSPENDED_EV"
    assert cs.offering_energy is True