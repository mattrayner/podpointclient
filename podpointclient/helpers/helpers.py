from distutils.log import error
from os import access
from typing import Any, Dict
import aiohttp
import async_timeout
import asyncio
import logging
import socket
from datetime import datetime
import re

from ..errors import APIError

TIMEOUT=10
HEADERS = {"Content-type": "application/json; charset=UTF-8"}

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Helpers:
    def auth_headers(self, access_token: str) -> Dict[str, str]:
        auth_header = {"Authorization": f"Bearer {access_token}"}
        combined_headers = HEADERS.copy()
        combined_headers.update(auth_header)
        return combined_headers

    def lazy_convert_to_datetime(self, date_string: str) -> datetime:
        if date_string is None or type(date_string) is not str:
            return None
        
        # Convert a 'Z' ending string to +00:00 for correct support
        date_string = re.sub(r"Z$", "+00:00", date_string)

        dt = None
        # Example: 2022-01-25T09:00:00+00:00
        try:
            dt = datetime.fromisoformat(date_string)
        except ValueError as e:
            _LOGGER.warning("Tried to convert '%s' to datetime but got: %s", date_string, e)
        
        return dt

    def lazy_iso_format_datetime(self, date_time: datetime) -> str:
        if type(date_time) is not datetime:
            return None

        return date_time.isoformat()

    def default_serialisation(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json()
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
            

class APIWrapper:
    def __init__(self, session: aiohttp.ClientSession, timeout: int = TIMEOUT) -> None:
        self._timeout: int = timeout
        self._session: aiohttp.ClientSession = session

    async def get(self, url: str, headers: Dict[str, Any], params: Dict[str, Any] = None, exception_class=APIError) -> aiohttp.ClientResponse:
        return await self.__wrapper(method="get", url=url, params=params, headers=headers, exception_class=exception_class)

    async def put(self, url: str, body: Any, headers: Dict[str, Any], params: Dict[str, Any] = None, exception_class=APIError) -> aiohttp.ClientResponse:
        return await self.__wrapper(method="put", url=url, params=params, data=body, headers=headers, exception_class=exception_class)
    
    async def post(self, url: str, body: Any, headers: Dict[str, Any], params: Dict[str, Any] = None, exception_class=APIError) -> aiohttp.ClientResponse:
        return await self.__wrapper(method="post", url=url, params=params, data=body, headers=headers, exception_class=exception_class)

    async def __wrapper(
        self,
        method: str,
        url: str,
        data: Dict[str, Any] = {},
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
        exception_class=APIError
    ) -> aiohttp.ClientResponse:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(self._timeout):
                response = None

                if method == "get":
                    response = await self._session.get(url, headers=headers, params=params)

                elif method == "put":
                    response = await self._session.put(url, headers=headers, json=data)

                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                else:
                    raise ValueError("Method '%s' not supported", method)

                if response is None:
                    raise APIError("Unexpected error from Pod Point API. Received a None response when querying.")

                if response.status < 200 or response.status > 202:
                    self.__handle_response_error(response=response, exception_class=exception_class)

                return response

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )
            raise exception

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
            raise exception

        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
            self.__handle_response_error(response=response, exception_class=exception_class)

        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened")
            raise exception

    async def __handle_response_error(self, response: aiohttp.ClientResponse, exception_class):
        status = response.status
        _LOGGER.error(f"Unexpected response when creating session ({status})")
        response = await response.text()
        _LOGGER.error(response)

        raise exception_class(status, response) 