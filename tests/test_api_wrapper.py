from urllib import response
import aiohttp
from podpointclient.helpers.helpers import APIWrapper
import pytest
from aioresponses import aioresponses

@pytest.mark.asyncio
async def test_get(aresponses):
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
    m.put('https://google.com/api/v1/test', body="OK")

    async with aiohttp.ClientSession() as session:
      wrapper = APIWrapper(session)
      async with await wrapper.put("https://google.com/api/v1/test", body={}, headers={}, params={"foo": "bar"}) as result:
        assert 200 == result.status
        assert "OK" == await result.text()