from argparse import _AttributeHolder
import logging

import aiohttp
from ..errors import SessionError
from ..endpoints import API_BASE_URL, SESSIONS
from .helpers import Helpers, APIWrapper

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Session:
    def __init__(self, email: str, password: str, access_token: str, session: aiohttp.ClientSession) -> None:
        self.email: str = email
        self.password: str = password
        self.access_token: str = access_token
        self.session_id: str = None
        self.user_id: str = None
        self._session: aiohttp.ClientSession = session
        self._helpers: Helpers = Helpers()

    async def create(self):
        url = f"{API_BASE_URL}{SESSIONS}"
        headers = self._helpers.auth_headers(self.access_token)
        payload = {"email": self.email, "password": self.password}

        return_value = False

        try:
            wrapper = APIWrapper(session=self._session)
            response = await wrapper.post(url, body=payload, headers=headers, exception_class=SessionError)

            json = await response.json()

            if json['sessions']:
                _LOGGER.debug("Setting session")
                self.user_id = json['sessions']['user_id']
                self.session_id = json['sessions']['id']
                return_value = True
        except KeyError as exception:
            _LOGGER.error(f"Error processing session response {exception}")
            raise SessionError(exception)

        return return_value