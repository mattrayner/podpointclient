"""Wrapper around calls to the pod point API"""
import asyncio
from typing import Any, Dict
import time
import logging
from socket import gaierror
import aiohttp
import async_timeout

from ..errors import APIError, AuthError, SessionError, ApiConnectionError

TIMEOUT=10
HEADERS = {"Content-type": "application/json; charset=UTF-8"}

_LOGGER: logging.Logger = logging.getLogger(__package__)


class APIWrapper:
    """Wrapper around calls to the pod point API"""
    def __init__(self, session: aiohttp.ClientSession, timeout: int = TIMEOUT) -> None:
        self._timeout: int = timeout
        self._session: aiohttp.ClientSession = session

    async def get(
        self,
        url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any] = None,
        exception_class=APIError
    ) -> aiohttp.ClientResponse:
        """Make a GET request"""
        return await self.__wrapper(
            method="get",
            url=url,
            params=params,
            headers=headers,
            exception_class=exception_class
        )

    async def put(
        self,
        url: str,
        body: Any,
        headers: Dict[str, Any],
        params: Dict[str, Any] = None,
        exception_class=APIError
    ) -> aiohttp.ClientResponse:
        """Make a PUT request"""
        return await self.__wrapper(
            method="put",
            url=url,
            params=params,
            data=body,
            headers=headers,
            exception_class=exception_class
        )

    async def post(
        self,
        url: str,
        body: Any,
        headers: Dict[str, Any],
        params: Dict[str, Any] = None,
        exception_class=APIError
    ) -> aiohttp.ClientResponse:
        """Make a POST request"""
        return await self.__wrapper(
            method="post",
            url=url,
            params=params,
            data=body,
            headers=headers,
            exception_class=exception_class
        )

    async def delete(
        self,
        url: str,
        headers: Dict[str, Any],
        params: Dict[str, Any] = None,
        exception_class=APIError
    ) -> aiohttp.ClientResponse:
        """Make a GET request"""
        return await self.__wrapper(
            method="delete",
            url=url,
            params=params,
            headers=headers,
            exception_class=exception_class
        )

    async def __wrapper(
        self,
        method: str,
        url: str,
        data: Dict[str, Any] = None,
        headers: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
        exception_class=APIError
    ) -> aiohttp.ClientResponse:
        """Get information from the API."""
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        try:
            async with async_timeout.timeout(self._timeout):
                start_time = time.time()
                _LOGGER.debug("%s %s %s %s",method.upper(), url, params, data)

                response = None

                if method == "get":
                    response = await self._session.get(url, headers=headers, params=params)

                elif method == "put":
                    response = await self._session.put(
                        url,
                        headers=headers,
                        params=params,
                        json=data
                    )

                elif method == "post":
                    if isinstance(data, str):
                        response = await self._session.post(
                            url,
                            headers=headers,
                            params=params,
                            data=data
                        )
                    else:
                        response = await self._session.post(
                            url,
                            headers=headers,
                            params=params,
                            json=data
                        )

                elif method == "delete":
                    response = await self._session.delete(url, headers=headers, params=params)

                else:
                    raise ValueError(f'Method \'{method}\' not supported')

                if response is None:
                    raise APIError(
                        "Unexpected error from Pod Point API. \
Received a None response when querying."
                    )

                end_time = time.time()
                _LOGGER.debug("%s - %ss", response.status, end_time - start_time)

                if response.status < 200 or response.status > 204:
                    await self.__handle_response_error(
                        response=response,
                        exception_class=exception_class
                    )

                return response

        except asyncio.TimeoutError as exception:
            message = f"Timeout error fetching information from {url} - {exception}"
            raise ApiConnectionError(message) from exception

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
            raise exception

        except (aiohttp.ClientError, gaierror) as exception:
            message = f"Error connecting to Pod Point ({url}) - {exception}"
            raise ApiConnectionError(message) from exception

        except (AuthError, SessionError) as exception:
            _LOGGER.error(
                "Authentication error when creating auth or session. (%s)",
                type(exception)
            )
            raise exception

        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened")
            raise exception

    async def __handle_response_error(self, response: aiohttp.ClientResponse, exception_class):
        status = response.status
        response = await response.text()

        raise exception_class(status, response)
