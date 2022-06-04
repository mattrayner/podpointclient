"""Auth module for pod point, handled access token lifecycle."""

import logging
from datetime import datetime, timedelta

import aiohttp

from ..errors import APIError, AuthError, SessionError
from .session import Session
from ..endpoints import API_BASE_URL, AUTH
from .functions import HEADERS
from .api_wrapper import APIWrapper

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Auth():
    """Manages authentication lifecycle for a user"""
    def __init__(self, email: str, password: str, session: aiohttp.ClientSession):
        self.email: str = email
        self.password: str = password
        self.access_token: str = None
        self.access_token_expiry: datetime = None
        self._session: aiohttp.ClientSession = session
        self._api_wrapper: APIWrapper = APIWrapper(session=self._session)

    @property
    def user_id(self):
        """Return the user_id for a given session"""
        if self._session:
            return self._session.user_id
        return None

    def check_access_token(self) -> bool:
        """Does the current access token need refreshing?"""
        access_token_set: bool = (
            self.access_token is not None and self.access_token_expiry is not None
        )
        access_token_not_expired: bool = (
            access_token_set and datetime.now() < self.access_token_expiry
        )

        return bool(access_token_set and access_token_not_expired)

    async def async_update_access_token(self) -> bool:
        """Update access token, if needed."""
        if self.check_access_token():
            return True

        try:
            session_created: bool = False
            _LOGGER.debug('Updating access token')
            access_token_updated: bool = await self.__update_access_token()

            if access_token_updated:
                _LOGGER.debug(
                    "Updated access token. New expiration: %s",
                    self.access_token_expiry
                )

                self._session = Session(
                    email=self.email,
                    password=self.password,
                    access_token=self.access_token,
                    session=self._session
                )
                session_created = await self._session.create()

                if session_created is False:
                    _LOGGER.error("Error creating session")
            else:
                _LOGGER.error("Error updating access token")

            return access_token_updated and session_created
        except AuthError as exception:
            _LOGGER.error("Error updating access token. %s", exception)
            raise exception
        except SessionError as exception:
            _LOGGER.error("Error creating session. %s", exception)
            raise exception

    async def __update_access_token(self) -> bool:
        return_value = False

        url = f"{API_BASE_URL}{AUTH}"
        payload = {"username": self.email, "password": self.password}

        try:
            wrapper = APIWrapper(session=self._session)
            response = await wrapper.post(
                url,
                body=payload,
                headers=HEADERS,
                exception_class=AuthError)

            if response.status != 200:
                await self.__handle_response_error(response, AuthError)

            json = await response.json()
            self.access_token = json["access_token"]
            self.access_token_expiry = datetime.now() + timedelta(
                seconds=json["expires_in"] - 10
            )
            return_value = True
        except AuthError as exception:
            raise exception
        except KeyError as exception:
            raise AuthError(
                response.status,
                f"Error processing access token response. {exception} not found in json."
            ) from exception
        except TypeError as exception:
            raise AuthError(
                response.status,
                f"Error processing access token response. \
When calculating expiry date, got: {exception}."
            ) from exception
        except APIError as exception:
            raise exception

        return return_value

    async def __handle_response_error(self, response, error_class):
        status = response.status
        response = await response.text()

        raise error_class(status, response)
