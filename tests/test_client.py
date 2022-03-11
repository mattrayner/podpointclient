import imp
from aioresponses import aioresponses
import aiohttp
import json
from podpointclient.client import PodPointClient
from typing import List
from podpointclient.pod import Pod
import pytest

from podpointclient.endpoints import API_BASE_URL, AUTH, CHARGE_SCHEDULES, PODS, SESSIONS, UNITS, USERS

@pytest.mark.asyncio
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
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules&perpage=all', payload=pods_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session)
            pods = await client.async_get_pods()
            assert 1 == len(pods)
            assert list == type(pods)
            assert Pod == type(pods[0])

@pytest.mark.asyncio
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
        m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?include=statuses%252Cprice%252Cmodel%252Cunit_connectors%252Ccharge_schedules&perpage=all', payload=pods_response)
        m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}', status=201, payload=schedules_response)

        async with aiohttp.ClientSession() as session:
            client = PodPointClient(username="1233", password="1234", session=session)
            resp = await client.async_set_schedule(True, Pod(data=pod_data))
            assert True == resp
