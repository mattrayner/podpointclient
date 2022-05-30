from datetime import datetime, timedelta
from timeit import repeat
from unittest.mock import AsyncMock, MagicMock
from podpointclient.errors import AuthError, SessionError
from podpointclient.helpers.auth import Auth
import aiohttp
import asyncio
from aioresponses import aioresponses
import logging

from podpointclient.endpoints import API_BASE, API_BASE_URL, API_VERSION, AUTH, SESSIONS

import pytest

EMAIL: str = 'test@example.com'
PASSWORD: str = 'passw0rd!'

def subject(session) -> Auth:
    return Auth(email=EMAIL, password=PASSWORD, session=session)

def complete_subject(session) -> Auth:
    auth = subject(session)
    auth.access_token = "1234"
    auth.access_token_expiry = datetime.now() + timedelta(minutes=10)

    return auth

def expired_subject(session) -> Auth:
    auth = complete_subject(session)
    auth.access_token_expiry = datetime.now() - timedelta(minutes=10)

    return auth

async def test_access_token_valid():
    async with aiohttp.ClientSession() as session:
        auth = complete_subject(session)
    
        assert auth.check_access_token() is True

async def test_access_token_expired():
    async with aiohttp.ClientSession() as session:
        auth = expired_subject(session)
    
        assert auth.check_access_token() is False

async def test_access_token_not_set():
    async with aiohttp.ClientSession() as session:
        # No values set
        auth = subject(session)
        assert auth.check_access_token() is False

        # Not expired, but not set
        auth = subject(session)
        auth._access_token_expiry = datetime.now() + timedelta(minutes=10)
        assert auth.check_access_token() is False

        # Set but no exiry
        auth = subject(session)
        auth._access_token = "1234"
        assert auth.check_access_token() is False

@pytest.mark.asyncio
async def test_update_access_token_when_not_set(aiohttp_client):
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
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)

        async with aiohttp.ClientSession() as session:
            auth = subject(session)

            result = await auth.async_update_access_token()
            print(result)
            print(auth)

            assert result is True
            assert auth.access_token == "1234"
            assert auth.access_token_expiry > datetime.now()

@pytest.mark.asyncio
async def test_update_access_token_when_not_set(aiohttp_client):
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
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)

        async with aiohttp.ClientSession() as session:
            auth = expired_subject(session)
            assert auth.access_token_expiry < datetime.now()

            m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
            m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)

            result2 = await auth.async_update_access_token()
            assert result2 is True
            assert auth.access_token == "1234"
            assert auth.access_token_expiry > datetime.now()

async def test_update_access_token_when_token_valid():
    async with aiohttp.ClientSession() as session:
        auth = complete_subject(session)
        assert await auth.async_update_access_token() is True

async def test_auth_401_error():
    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', status=401 , body="foo error")

        async with aiohttp.ClientSession() as session:
            auth = expired_subject(session)

            with pytest.raises(AuthError) as exc_info:   
                await auth.async_update_access_token()

            assert "Auth Error (401) - foo error" in str(exc_info.value)

async def test_auth_json_error():
    # MISSING ELEMENT
    auth_response = {
        "token_type": "Bearer",
        "expires_in": "a74f3",
        "refresh_token": "1234"
    }

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)

        async with aiohttp.ClientSession() as session:
            auth = expired_subject(session)

            with pytest.raises(AuthError) as exc_info:   
                await auth.async_update_access_token()

            assert "Auth Error (200) - Error processing access token response. 'access_token' not found in json." in str(exc_info.value)

    # INVALID EXPIRES_IN
    auth_response = {
        "token_type": "Bearer",
        "expires_in": "F14A3",
        "access_token": "1234",
        "refresh_token": "1234"
    }

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)

        async with aiohttp.ClientSession() as session:
            auth = expired_subject(session)

            with pytest.raises(AuthError) as exc_info:   
                await auth.async_update_access_token()

            assert "Auth Error (200) - Error processing access token response. When calculating expiry date, got: unsupported operand type(s) for -: 'str' and 'int'." in str(exc_info.value)


async def test_session_401_error():
    auth_response = {
        "token_type": "Bearer",
        "expires_in": 1234,
        "access_token": "1234",
        "refresh_token": "1234"
    }

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', status=401, body="bar error")

        async with aiohttp.ClientSession() as session:
            auth = expired_subject(session)

            with pytest.raises(SessionError) as exc_info:   
                await auth.async_update_access_token()

            assert "Session Error (401) - bar error" in str(exc_info.value)

async def test_session_json_error():
    auth_response = {
        "token_type": "Bearer",
        "expires_in": 1234,
        "access_token": "1234",
        "refresh_token": "1234"
    }
    session_response = {
        "sessions": {
            "user_id": "1234"
        }
    }

    with aioresponses() as m:
        m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)

        async with aiohttp.ClientSession() as session:
            auth = expired_subject(session)

            with pytest.raises(SessionError) as exc_info:   
                await auth.async_update_access_token()

            assert "Session Error (200) - Error processing session response. Unable to find key: 'id' within json." in str(exc_info.value)

def test_auth_no_session():
    auth = Auth(email=EMAIL, password=PASSWORD, session=False)
    assert auth.user_id == None
