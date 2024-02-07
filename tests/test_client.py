import imp

from aioresponses import aioresponses
import aiohttp
from podpointclient.client import PodPointClient
from typing import List
from podpointclient.pod import Pod, Firmware
from podpointclient.charge import Charge
from podpointclient.charge_override import ChargeOverride
from podpointclient.user import User
from podpointclient.errors import ChargeOverrideValidationError
import pytest
from freezegun import freeze_time
import json
import pytz
from datetime import timedelta

from podpointclient.endpoints import GOOGLE_BASE_URL, PASSWORD_VERIFY, API_BASE_URL, AUTH, CHARGE_SCHEDULES, CHARGES, FIRMWARE, PODS, SESSIONS, UNITS, USERS, CHARGE_OVERRIDE

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_credentials_verified():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }
    
    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=&perpage=1&page=1&timestamp=1640995200.0', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            pods = await client.async_credentials_verified()
            assert pods is True

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_credentials_verified_returns_false_if_no_pods():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": []
    }
    
    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=&perpage=1&page=1&timestamp=1640995200.0', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            pods = await client.async_credentials_verified()
            assert pods is False

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_credentials_verified_returns_false_if_body_unexpected():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = { "foo": "bar" }
    
    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=&perpage=1&page=1&timestamp=1640995200.0', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            pods = await client.async_credentials_verified()
            assert pods is False

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_pods_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=5&page=1&timestamp=1640995200.0', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            pods = await client.async_get_pods()
            assert 1 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])

@pytest.mark.asyncio
async def test_async_get_pods_response_without_timestamp():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=5&page=1', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=False)
            pods = await client.async_get_pods()
            assert 1 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])

@pytest.mark.asyncio
async def test_async_get_all_pods_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }
    pods_response_short = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=5&page=1', payload=pods_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=5&page=2', payload=pods_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=5&page=3', payload=pods_response_short)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=False)
            pods = await client.async_get_all_pods()
            assert 13 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_all_pods_response_with_includes_overridden_and_timestamp():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }
    pods_response_short = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=foo%252Cbar&perpage=5&page=1&timestamp=1640995200.0', payload=pods_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=foo%252Cbar&perpage=5&page=2&timestamp=1640995200.0', payload=pods_response_short)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            pods = await client.async_get_all_pods(includes=["foo", "bar"])
            assert 8 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])
            
@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_all_pods_response_with_includes_empty_and_timestamp():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }
    pods_response_short = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json')),
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=5&page=1&timestamp=1640995200.0', payload=pods_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=5&page=2&timestamp=1640995200.0', payload=pods_response_short)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            pods = await client.async_get_all_pods(includes=[])
            assert 8 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_schedules_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pod_data = json.load(open('./tests/fixtures/complete_pod.json'))
    pods_response = {
        "pods": [
            pod_data
        ]
    }
    schedules_response = json.load(open('./tests/fixtures/create_schedules.json'))

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=all&timestamp=1640995200.0', payload=pods_response)
        m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}?timestamp=1640995200.0', status=201, payload=schedules_response)
        m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}?timestamp=1640995200.0', status=200, payload=schedules_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            resp = await client.async_set_schedule(True, Pod(data=pod_data))
            assert True == resp

            resp = await client.async_set_schedule(True, Pod(data=pod_data))
            assert False == resp

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_charges_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    charges_reponse = json.load(open('./tests/fixtures/complete_charges.json'))
    charges_reponse_small = json.load(open('./tests/fixtures/small_charges.json'))
    charges_reponse_small_page_2 = json.load(open('./tests/fixtures/small_charges_page_2.json'))
    charges_reponse_med = json.load(open('./tests/fixtures/med_charges.json'))
    charges_reponse_empty = json.load(open('./tests/fixtures/charges_empty.json'))

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=all&page=1&timestamp=1640995200.0', payload=charges_reponse)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=5&page=1&timestamp=1640995200.0', payload=charges_reponse_small)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=5&page=2&timestamp=1640995200.0', payload=charges_reponse_small_page_2)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=5&page=42&timestamp=1640995200.0', payload=charges_reponse_empty)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=10&page=1&timestamp=1640995200.0', payload=charges_reponse_med)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            
            # Test that by default we request 5 Charge items
            resp: List[Charge] = await client.async_get_charges()
            assert 5 == len(resp)
            assert Charge == type(resp[0])

            # Test that a request for 10 will result in 10
            resp: List[Charge] = await client.async_get_charges(perpage=10)
            assert 10 == len(resp)

            # Test that a request for all will result in all
            resp: List[Charge] = await client.async_get_charges(perpage="all")
            assert 10 == len(resp)

            # Test that pages work as expected
            resp: List[Charge] = await client.async_get_charges(perpage=5, page=2)
            assert 5 == len(resp)
            assert 6 == resp[0].id

            # Test that requesting a page that is out of bounds returns an empty list
            resp: List[Charge] = await client.async_get_charges(perpage=5, page=42)
            assert 0 == len(resp)

async def test__schedule_data():
    async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            true_data = {
                'data': [
                    {
                        'end_day': 1,
                        'end_time': '00:00:01',
                        'start_day': 1,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                    {
                        'end_day': 2,
                        'end_time': '00:00:01',
                        'start_day': 2,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                    {
                        'end_day': 3,
                        'end_time': '00:00:01',
                        'start_day': 3,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                    {
                        'end_day': 4,
                        'end_time': '00:00:01',
                        'start_day': 4,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                    {
                        'end_day': 5,
                        'end_time': '00:00:01',
                        'start_day': 5,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                    {
                        'end_day': 6,
                        'end_time': '00:00:01',
                        'start_day': 6,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                    {
                        'end_day': 7,
                        'end_time': '00:00:01',
                        'start_day': 7,
                        'start_time': '00:00:00',
                        'status': {'is_active': True}
                    },
                ]
            }
            false_data = {
                'data': [
                    {
                        'end_day': 1,
                        'end_time': '00:00:01',
                        'start_day': 1,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                    {
                        'end_day': 2,
                        'end_time': '00:00:01',
                        'start_day': 2,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                    {
                        'end_day': 3,
                        'end_time': '00:00:01',
                        'start_day': 3,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                    {
                        'end_day': 4,
                        'end_time': '00:00:01',
                        'start_day': 4,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                    {
                        'end_day': 5,
                        'end_time': '00:00:01',
                        'start_day': 5,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                    {
                        'end_day': 6,
                        'end_time': '00:00:01',
                        'start_day': 6,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                    {
                        'end_day': 7,
                        'end_time': '00:00:01',
                        'start_day': 7,
                        'start_time': '00:00:00',
                        'status': {'is_active': False}
                    },
                ]
            }
            assert client._schedule_data(True) == true_data
            assert client._schedule_data(False) == false_data

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_firmware():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pod_data = json.load(open('./tests/fixtures/complete_pod.json'))
    firmware_response = json.load(open('./tests/fixtures/complete_firmware.json'))

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{UNITS}/198765{FIRMWARE}?timestamp=1640995200.0', payload=firmware_response)
        m.get(f'{API_BASE_URL}{UNITS}/198765{FIRMWARE}', payload=firmware_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            resp = await client.async_get_firmware(pod=Pod(data=pod_data))
            assert 1 == len(resp)
            assert isinstance(resp[0], Firmware) is True

            firmware = resp[0]
            assert firmware.serial_number == '123456789'
            assert firmware.version_info.manifest_id == 'A30P-3.1.22-00001'
            assert firmware.update_status.is_update_available == False

            assert firmware.firmware_version == 'A30P-3.1.22-00001'
            assert firmware.update_available == False

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_user():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    user_data = json.load(open('./tests/fixtures/complete_user.json'))
    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{AUTH}?include=account,vehicle,vehicle.make,unit.pod.unit_connectors,unit.pod.statuses,unit.pod.model,unit.pod.charge_schedules,unit.pod.charge_override&timestamp=1640995200.0', payload=user_data)
        m.get(f'{API_BASE_URL}{AUTH}?include=account,vehicle,vehicle.make,unit.pod.unit_connectors,unit.pod.statuses,unit.pod.model,unit.pod.charge_schedules,unit.pod.charge_override', payload=user_data)
        m.get(f'{API_BASE_URL}{AUTH}?include=account', payload=user_data)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            user = await client.async_get_user()
            assert isinstance(user, User) is True

            assert user.id == 123456

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_schedules_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    pod_data = json.load(open('./tests/fixtures/complete_pod.json'))
    pods_response = {
        "pods": [
            pod_data
        ]
    }
    schedules_response = json.load(open('./tests/fixtures/create_schedules.json'))

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules%252Ccharge_override&perpage=all&timestamp=1640995200.0', payload=pods_response)
        m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}?timestamp=1640995200.0', status=201, payload=schedules_response)
        m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}?timestamp=1640995200.0', status=200, payload=schedules_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            resp = await client.async_set_schedule(True, Pod(data=pod_data))
            assert True == resp

            resp = await client.async_set_schedule(True, Pod(data=pod_data))
            assert False == resp

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_all_charges_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    charges_reponse_large = json.load(open('./tests/fixtures/large_charges.json'))
    charges_reponse_small_page_2 = json.load(open('./tests/fixtures/small_charges_page_2.json'))

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=50&page=1&timestamp=1640995200.0', payload=charges_reponse_large)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=50&page=2&timestamp=1640995200.0', payload=charges_reponse_small_page_2)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True, http_debug=True)
            
            # Test that by default we request 5 Charge items
            resp: List[Charge] = await client.async_get_all_charges()
            assert 55 == len(resp)
            assert Charge == type(resp[0])

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_charge_override_with_an_empty_response_meaning_smart_mode():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', body="", status=204)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_get_charge_override(pod=Pod(data={"unit_id": 1234}))
            assert override is None

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_charge_override_with_a_manual_mode_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    override_response = {
        "ppid": "PSL-123456",
        "requested_at": "2021-12-31T16:22:34.000Z",
        "received_at": "2021-12-31T16:22:43.000Z",
        "ends_at": None
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', payload=override_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_get_charge_override(pod=Pod(data={"unit_id": 1234}))
            assert override is not None
            assert ChargeOverride == type(override)
            assert override.active is False
            assert override.remaining_time is None

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_charge_override_with_a_charge_override_time_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    override_response = {
        "ppid": "PSL-123456",
        "requested_at": "2021-12-31T16:22:34.000Z",
        "received_at": "2021-12-31T16:22:43.000Z",
        "ends_at": "2022-01-01T03:00:00.000Z"
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', payload=override_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_get_charge_override(pod=Pod(data={"unit_id": 1234}))
            assert override is not None
            assert ChargeOverride == type(override)
            assert override.active is True
            assert override.remaining_time == timedelta(hours=3)

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_charge_override_with_a_time_set():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    override_response = {
        "ppid": "PSL-123456",
        "requested_at": "2022-01-01T00:00:00.000Z",
        "received_at": "2022-01-01T00:00:00.000Z",
        "ends_at": "2022-01-01T03:02:01.000Z"
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.put(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', status=201, payload=override_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_set_charge_override(pod=Pod(data={"unit_id": 1234}), hours=3, minutes=2, seconds=1)
            assert override is not None
            assert ChargeOverride == type(override)
            assert override.active is True
            assert override.remaining_time == timedelta(hours=3, minutes=2, seconds=1)

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_charge_override_with_an_invalid_time_set():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    override_response = {
        "ppid": "PSL-123456",
        "requested_at": "2022-01-01T00:00:00.000Z",
        "received_at": "2022-01-01T00:00:00.000Z",
        "ends_at": "2022-01-01T03:02:01.000Z"
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.put(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', status=201, payload=override_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)

            with pytest.raises(ChargeOverrideValidationError):
                await client.async_set_charge_override(pod=Pod(data={"unit_id": 1234}), hours=-3, minutes=0, seconds="a")
            
@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_charge_mode_manual_with_expected_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    override_response = {
        "ppid": "PSL-123456",
        "requested_at": "2022-01-01T00:00:00.000Z",
        "received_at": "2022-01-01T00:00:00.000Z",
        "ends_at": None
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.put(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', status=201, payload=override_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_set_charge_mode_manual(pod=Pod(data={"ppid": "PSL-123456", "unit_id": 1234}))
            assert override == True

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_charge_mode_manual_with_unexpected_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }
    override_response = {}

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.put(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', status=201, payload=override_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_set_charge_mode_manual(pod=Pod(data={"ppid": "PSL-123456", "unit_id": 1234}))
            assert override == False


@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_charge_mode_smart_with_204_response():
    auth_response = {
        "token_type": "Bearer",
        "expires_in": 1234,
        "access_token": "1234",
        "refresh_token": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.delete(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', status=204)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_set_charge_mode_smart(pod=Pod(data={"unit_id": 1234}))
            assert override is True

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_charge_mode_smart_with_unexpected_response():
    auth_response = {
        "idToken": "1234",
        "expiresIn": "1234",
        "refreshToken": "1234"
    }
    session_response = {
        "sessions": {
            "id": "1234",
            "user_id": "1234"
        }
    }

    with aioresponses() as m:
        m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.delete(f'{API_BASE_URL}{UNITS}/1234{CHARGE_OVERRIDE}?timestamp=1640995200.0', status=200)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session, include_timestamp=True)
            override = await client.async_set_charge_mode_smart(pod=Pod(data={"unit_id": 1234}))
            assert override is False
