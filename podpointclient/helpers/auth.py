import logging
from datetime import datetime, timedelta

import aiohttp

from ..errors import AuthError, SessionError
from .session import Session
from ..endpoints import API_BASE_URL, AUTH
from .helpers import APIWrapper, HEADERS

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

        if access_token_set and access_token_not_expired:
            return True
        else:
            return False

    async def async_update_access_token(self) -> bool:
        """Update access token, if needed."""
        _LOGGER.debug(self.check_access_token())
        if self.check_access_token():
            return True

        try:
            session_created: bool = False
            _LOGGER.debug('Updating access token')
            access_token_updated: bool = await self.__update_access_token()
            _LOGGER.debug('Done')

            if access_token_updated:
                _LOGGER.debug(
                    f"Updated access token. New expiration: {self.access_token_expiry}"
                )

                self._session = Session(email=self.email, password=self.password, access_token=self.access_token, session=self._session)
                session_created = await self._session.create()

                if session_created is False:
                    _LOGGER.error("Error creating session")
            else:
                _LOGGER.error("Error updating access token")

            _LOGGER.debug("Going to return with:")
            _LOGGER.debug((access_token_updated and session_created))
            _LOGGER.debug(access_token_updated)
            _LOGGER.debug(session_created)

            return (access_token_updated and session_created)
        except AuthError as exception:
            _LOGGER.error("Error updating access token. %s", exception)
        except SessionError as exception:
            _LOGGER.error("Error creating session. %s", exception)

    async def __update_access_token(self) -> bool:
        return_value = False

        _LOGGER.info("Updating Pod Point access token")

        url = f"{API_BASE_URL}{AUTH}"
        payload = {"username": self.email, "password": self.password}

        try:
            print(url)
            print(payload)
            print(HEADERS)

            _LOGGER.debug('Posting to wrapper')
            wrapper = APIWrapper(session=self._session)
            response = await wrapper.post(url, body=payload, headers=HEADERS)

            _LOGGER.debug(response)

            if response.status != 200:
                await self.__handle_response_error(response, AuthError)
            else:
                json = await response.json()
                _LOGGER.debug(json)
                self.access_token = json["access_token"]
                self.access_token_expiry = datetime.now() + timedelta(
                    seconds=json["expires_in"] - 10
                )
                return_value = True
        except KeyError as exception:
            _LOGGER.error(f"Error processing access token response: {exception}")
            await self.__handle_response_error(response, SessionError)

        return return_value

    async def __handle_response_error(self, response, error_class):
        status = response.status
        _LOGGER.error(f"Unexpected response when creating session ({status})")
        response = await response.text()
        _LOGGER.error(response)

        raise error_class(status, response)
