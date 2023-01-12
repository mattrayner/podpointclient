"""Session module handled session lifecycle"""
import logging
import aiohttp
from .functions import auth_headers

from ..errors import SessionError
from ..endpoints import API_BASE_URL, SESSIONS
from .api_wrapper import APIWrapper

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Session:
    """Session lifecycle handler"""
    def __init__(
        self,
        email: str,
        password: str,
        access_token: str,
        session: aiohttp.ClientSession,
        http_debug: bool = None
    ) -> None:
        self.email: str = email
        self.password: str = password
        self.access_token: str = access_token
        self.session_id: str = None
        self.user_id: str = None
        self._session: aiohttp.ClientSession = session
        self._http_debug: bool = http_debug if http_debug is not None else False

    async def create(self):
        """Create a session using credentials passed in initialisation"""
        return_value = False

        try:
            wrapper = APIWrapper(session=self._session)
            response = await wrapper.post(
                url=f"{API_BASE_URL}{SESSIONS}",
                body={"email": self.email, "password": self.password},
                headers=auth_headers(self.access_token),
                exception_class=SessionError
            )

            json = await response.json()

            if self._http_debug:
                _LOGGER.debug(json)

            if json.get('sessions', None):
                self.user_id = json['sessions']['user_id']
                self.session_id = json['sessions']['id']
                return_value = True
        except KeyError as exception:
            raise SessionError(
                response.status,
                f"Error processing session response. Unable to find key: {exception} within json."
            ) from exception

        return return_value
