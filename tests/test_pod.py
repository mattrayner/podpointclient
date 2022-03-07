from calendar import month
from email.mime import image
from pprint import PrettyPrinter
from aiohttp import JsonPayload
import podpointclient
from podpointclient.pod import Pod, Socket, StatusKeyName, StatusName
import json
from datetime import datetime, timezone, timedelta
import pytz

from podpointclient.schedule import Schedule, ScheduleStatus


def load_fixture(name: str) -> JsonPayload:
    f = open(f'./tests/fixtures/{name}.json')
    return json.load(f)


def complete_pod_fixture():
    return load_fixture('complete_pod')


def test_empty_pod():
    pod = Pod(data={})
    assert pod.id == None
    assert pod.name == None
    assert pod.ppid == None
    assert pod.payg == None
    assert pod.home == None
    assert pod.public == None
    assert pod.ev_zone == None
    assert pod.location == Pod.Location(lat=0.0, lng=0.0)
    assert pod.address_id == None
    assert pod.description == ""
    assert pod.commissioned_at == None
    assert pod.created_at == None
    assert pod.last_contact_at == None
    assert pod.contactless_enabled == None
    assert pod.unit_id == None
    assert pod.timezone == None
    assert pod.model == Pod.Model(
        id=None,
        name=None,
        vendor=None,
        supports_payg=False,
        supports_ocpp=False,
        supports_contactless=False,
        image_url=None
    )
    assert pod.price == None
    assert pod.statuses == []
    assert pod.unit_connectors == []
    assert pod.charge_schedules == []


def test_happy_path():
    pod = Pod(data=complete_pod_fixture())

    assert 113113 == pod.id
    assert "Foo Pod" == pod.name
    assert "PSL-254321" == pod.ppid
    assert pod.payg is False
    assert pod.home is True
    assert pod.public is False
    assert pod.ev_zone is False

    assert pod.location == Pod.Location(lat=51.4995, lng=0.1248)
    assert 51.4995 == pod.location.lat
    assert 0.1248 == pod.location.lng

    assert 987 == pod.address_id
    assert "My pod description" == pod.description

    assert datetime(
        year=2022,
        month=1,
        day=1,
        hour=9,
        minute=0,
        second=0,
        tzinfo=timezone.utc
    ) == pod.commissioned_at
    assert datetime(
        year=2022,
        month=2,
        day=1,
        hour=10,
        minute=0,
        second=0,
        tzinfo=timezone.utc
    ) == pod.created_at

    assert datetime(
        year=2022,
        month=1,
        day=11,
        hour=2,
        minute=15,
        second=59,
        tzinfo=timezone(timedelta(seconds=3600))
    ) == pod.last_contact_at

    assert pod.contactless_enabled is False

    assert 198765 == pod.unit_id
    assert "UTC" == pod.timezone

    assert pod.model == Pod.Model(
        id=123,
        name="S7-UC-03-ACA",
        vendor="Pod Point",
        supports_payg=False,
        supports_ocpp=False,
        supports_contactless=False,
        image_url=None
    )
    assert "S7-UC-03-ACA" == pod.model.model

    assert pod.price is None
    assert 1 == len(pod.statuses)
    assert pod.statuses == [
        Pod.Status(
            id=2,
            name=StatusName.CHARGING,
            key_name=StatusKeyName.CHARGING,
            label=StatusName.CHARGING,
            door="A",
            door_id=1
        )
    ]

    assert 1 == len(pod.unit_connectors)
    assert pod.unit_connectors == [
        Pod.Connector(
            id=123,
            door="A",
            door_id=1,
            power=7,
            current=32,
            voltage=230,
            charge_method="Single Phase AC",
            has_cable=False,
            socket=Socket(
                type="IEC 62196-2 Type 2",
                description="Type 2 socket",
                ocpp_name="sType2",
                ocpp_code=3
            )
        )
    ]

    assert 7 == len(pod.charge_schedules)
    assert pod.charge_schedules == [
        Schedule(
            uid="a18eb318-f84b-48a8-9f84-e5cb44e32b16",
            start_day=1,
            start_time="00:00:00",
            end_day=1,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=True)
        ),
        Schedule(
            uid="ec1a9a6c-bb4e-4435-a676-06eea8fd8f1a",
            start_day=2,
            start_time="00:00:00",
            end_day=2,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=True)
        ),
        Schedule(
            uid="c5447a64-0aeb-4e1e-9af1-c5e13b7acf0c",
            start_day=3,
            start_time="00:00:00",
            end_day=3,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=True)
        ),
        Schedule(
            uid="8de14592-47f8-4102-a2a8-ef0638a97eb8",
            start_day=4,
            start_time="00:00:00",
            end_day=4,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=True)
        ),
        Schedule(
            uid="8e7ff42e-d1a4-4fa1-985f-7a5768d16852",
            start_day=5,
            start_time="00:00:00",
            end_day=5,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=False)
        ),
        Schedule(
            uid="dfa4d6e5-fb69-43d1-85b1-41c818f6940e",
            start_day=6,
            start_time="00:00:00",
            end_day=6,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=False)
        ),
        Schedule(
            uid="fd378f0b-c91a-4377-ab02-7d668a505b5b",
            start_day=7,
            start_time="00:00:00",
            end_day=7,
            end_time="00:00:01",
            status=ScheduleStatus(is_active=False)
        ),
    ]


def test_serialisation():
    pod = Pod(data=complete_pod_fixture())

    expected = {'id': 113113, 'name': 'Foo Pod', 'ppid': 'PSL-254321', 'payg': False, 'home': True, 'public': False, 'evZone': False, 'location': {'lat': 51.4995, 'lng': 0.1248}, 'address_id': 987, 'description': 'My pod description', 'commissioned_at': '2022-01-01T09:00:00+00:00', 'created_at': '2022-02-01T10:00:00+00:00', 'last_contact_at': '2022-01-11T02:15:59+01:00', 'contactless_enabled': False, 'unit_id': 198765, 'timezone': 'UTC', 'model': {'id': 123, 'name': 'S7-UC-03-ACA', 'vendor': 'Pod Point', 'supports_payg': False, 'supports_ocpp': False, 'supports_contactless': False, 'image_url': None}, 'price': None, 'statuses': [{'id': 2, 'name': 'Charging', 'key_name': 'charging', 'label': 'Charging', 'door': 'A', 'door_id': 1}], 'unit_connectors': [{'connector': {'id': 123, 'door': 'A', 'door_id': 1, 'power': 7, 'current': 32, 'voltage': 230, 'charge_method': 'Single Phase AC', 'has_cable': False, 'socket': {'type': 'IEC 62196-2 Type 2', 'description': 'Type 2 socket', 'ocpp_name': 'sType2', 'ocpp_code': 3}}}], 'charge_schedules': [
        {'uid': 'a18eb318-f84b-48a8-9f84-e5cb44e32b16', 'start_day': 1, 'start_time': '00:00:00', 'end_day': 1, 'end_time': '00:00:01', 'status': {'is_active': True}}, {'uid': 'ec1a9a6c-bb4e-4435-a676-06eea8fd8f1a', 'start_day': 2, 'start_time': '00:00:00', 'end_day': 2, 'end_time': '00:00:01', 'status': {'is_active': True}}, {'uid': 'c5447a64-0aeb-4e1e-9af1-c5e13b7acf0c', 'start_day': 3, 'start_time': '00:00:00', 'end_day': 3, 'end_time': '00:00:01', 'status': {'is_active': True}}, {'uid': '8de14592-47f8-4102-a2a8-ef0638a97eb8', 'start_day': 4, 'start_time': '00:00:00', 'end_day': 4, 'end_time': '00:00:01', 'status': {'is_active': True}}, {'uid': '8e7ff42e-d1a4-4fa1-985f-7a5768d16852', 'start_day': 5, 'start_time': '00:00:00', 'end_day': 5, 'end_time': '00:00:01', 'status': {'is_active': False}}, {'uid': 'dfa4d6e5-fb69-43d1-85b1-41c818f6940e', 'start_day': 6, 'start_time': '00:00:00', 'end_day': 6, 'end_time': '00:00:01', 'status': {'is_active': False}}, {'uid': 'fd378f0b-c91a-4377-ab02-7d668a505b5b', 'start_day': 7, 'start_time': '00:00:00', 'end_day': 7, 'end_time': '00:00:01', 'status': {'is_active': False}}]}

    assert dict(pod) == expected
