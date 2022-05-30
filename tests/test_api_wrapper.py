from urllib import response
import aiohttp
from podpointclient.errors import APIError, ApiConnectionError
from podpointclient.helpers.helpers import APIWrapper
import pytest
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_get(aiohttp_client):
  with aioresponses() as m:
    m.get('https://google.com/api/v1/test', status=200, body="OK")

    async with aiohttp.ClientSession() as session:
      wrapper = APIWrapper(session)
      async with await wrapper.get("https://google.com/api/v1/test", headers={}) as result:
        assert 200 == result.status
        assert "OK" == await result.text()

@pytest.mark.asyncio
async def test_post(aiohttp_client):
  with aioresponses() as m:
    m.post('https://google.com/api/v1/test', body="OK")

    async with aiohttp.ClientSession() as session:
      wrapper = APIWrapper(session)
      async with await wrapper.post("https://google.com/api/v1/test", body={}, headers={}) as result:
        assert 200 == result.status
        assert "OK" == await result.text()

@pytest.mark.asyncio
async def test_put(aiohttp_client):
  with aioresponses() as m:
    m.put('https://google.com/api/v1/test?foo=bar', body="OK")

    async with aiohttp.ClientSession() as session:
      wrapper = APIWrapper(session)
      async with await wrapper.put("https://google.com/api/v1/test", body={}, headers={}, params={"foo": "bar"}) as result:
        assert 200 == result.status
        assert "OK" == await result.text()

@pytest.mark.asyncio
async def test_401(aiohttp_client):
  with aioresponses() as m:
    m.get('https://google.com/api/v1/test?foo=bar', status=401, body="AuthError")

    async with aiohttp.ClientSession() as session:
      wrapper = APIWrapper(session)

      with pytest.raises(APIError) as exc_info:   
        await wrapper.get("https://google.com/api/v1/test", headers={}, params={"foo": "bar"})

      assert "(401, 'AuthError')" in str(exc_info.value)

@pytest.mark.asyncio     
async def test_connection_errors(aiohttp_client):
  with aioresponses() as m:
    m.get('https://google.com/api/v1/test?foo=bar', timeout=True)

    async with aiohttp.ClientSession() as session:
      wrapper = APIWrapper(session)

      with pytest.raises(ApiConnectionError) as exc_info:   
        await wrapper.get("https://google.com/api/v1/test", headers={}, params={"foo": "bar"})

      assert "Connection Error: Timeout error fetching information from https://google.com/api/v1/test - Connection timeout test" in str(exc_info.value)
