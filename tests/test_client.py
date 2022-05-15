import imp
from aioresponses import aioresponses
import aiohttp
import json
from podpointclient.client import PodPointClient
from typing import List
from podpointclient.pod import Pod
from podpointclient.charge import Charge
import pytest
from freezegun import freeze_time

from podpointclient.endpoints import API_BASE_URL, AUTH, CHARGE_SCHEDULES, CHARGES, PODS, SESSIONS, UNITS, USERS

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_pods_response():
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
    pods_response = {
        "pods": [
            json.load(open('./tests/fixtures/complete_pod.json'))
        ]
    }

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules&perpage=all&timestamp=1640995200.0', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session)
            pods = await client.async_get_pods()
            assert 1 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_set_schedules_response():
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
    pod_data = json.load(open('./tests/fixtures/complete_pod.json'))
    pods_response = {
        "pods": [
            pod_data
        ]
    }
    schedules_response = json.load(open('./tests/fixtures/create_schedules.json'))

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules&perpage=all&timestamp=1640995200.0', payload=pods_response)
        m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}?timestamp=1640995200.0', status=201, payload=schedules_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session)
            resp = await client.async_set_schedule(True, Pod(data=pod_data))
            assert True == resp

@pytest.mark.asyncio
@freeze_time("Jan 1st, 2022")
async def test_async_get_charges_response():
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
    charges_reponse = json.load(open('./tests/fixtures/complete_charges.json'))
    charges_reponse_small = json.load(open('./tests/fixtures/small_charges.json'))
    charges_reponse_small_page_2 = json.load(open('./tests/fixtures/small_charges_page_2.json'))
    charges_reponse_med = json.load(open('./tests/fixtures/med_charges.json'))
    charges_reponse_empty = json.load(open('./tests/fixtures/charges_empty.json'))

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=all&page=1&timestamp=1640995200.0', payload=charges_reponse)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=5&page=1&timestamp=1640995200.0', payload=charges_reponse_small)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=5&page=2&timestamp=1640995200.0', payload=charges_reponse_small_page_2)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=5&page=42&timestamp=1640995200.0', payload=charges_reponse_empty)
        m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=10&page=1&timestamp=1640995200.0', payload=charges_reponse_med)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session)
            
            # Test that by default we request 5 Charge items
            resp: List[Charge] = await client.async_get_charges()
            assert 5 == len(resp)
            assert Charge == type(resp[0])

            # Test that a request for 10 will result in 10
            resp: List[Charge] = await client.async_get_charges(per_page=10)
            assert 10 == len(resp)

            # Test that a request for all will result in all
            resp: List[Charge] = await client.async_get_charges(per_page="all")
            assert 21 == len(resp)

            # Test that pages work as expected
            resp: List[Charge] = await client.async_get_charges(per_page=5, page=2)
            assert 5 == len(resp)
            assert 6 == resp[0].id

            # Test that requesting a page that is out of bounds returns an empty list
            resp: List[Charge] = await client.async_get_charges(per_page=5, page=42)
            assert 0 == len(resp)

async def test__schedule_data():
    async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session)
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