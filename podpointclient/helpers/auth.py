"""Auth module for pod point, handled access token lifecycle."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Callable

import aiohttp

from ..errors import APIError, AuthError, MfaError, MfaInvalidCode, MfaRequired, SessionError
from .session import Session
from ..endpoints import (
    GOOGLE_BASE_URL, PASSWORD_VERIFY, GOOGLE_TOKEN_BASE_URL, TOKEN,
    MFA_START, MFA_FINALIZE,
)
from .functions import HEADERS
from .api_wrapper import APIWrapper

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Auth():
    """Manages authentication lifecycle for a user"""
    def __init__(
        self,
        email: str,
        password: str,
        session: aiohttp.ClientSession,
        http_debug: bool = None,
        refresh_token: str = None,
        on_refresh_token: Callable[[str], None] = None,
    ):
        self.email: str = email
        self.password: str = password
        self.access_token: str = None
        self.refresh_token: str = refresh_token
        self._on_refresh_token = on_refresh_token
        self._token_lock = asyncio.Lock()
        self._mfa_pending_credential = None
        self._mfa_enrollment_id = None
        self._mfa_session_info = None
        self.access_token_expiry: datetime = None
        self.session: Session = None
        self._session: aiohttp.ClientSession = session
        self._api_wrapper: APIWrapper = APIWrapper(session=self._session)
        self._http_debug: bool = http_debug if http_debug is not None else False

    @property
    def user_id(self):
        """Return the user_id for a given session"""
        if self.session:
            return self.session.user_id
        return None

    def check_access_token(self) -> bool:
        """Does the current access token need refreshing?"""
        access_token_not_expired: bool = self.access_token_expired() is False

        return bool(self.access_token_set() and access_token_not_expired)

    def access_token_set(self) -> bool:
        return (
                self.access_token is not None and self.access_token_expiry is not None
        )

    def access_token_expired(self) -> bool:
        """Is the current access token expired"""
        return self.access_token_set() and datetime.now() > self.access_token_expiry

    async def async_update_access_token(self) -> bool:
        """Update access token, if needed."""
        async with self._token_lock:
            if self.check_access_token():
                return True
            return await self._async_update_session()

    async def _async_update_session(self) -> bool:
        try:
            _LOGGER.debug('Updating access token')
            access_token_updated: bool = await self.__update_access_token(
                refresh=bool(self.refresh_token) or self.access_token_expired()
            )

            _LOGGER.debug(
                "Updated access token. New expiration: %s",
                self.access_token_expiry
            )

            self.session = Session(
                email=self.email,
                password=self.password,
                access_token=self.access_token,
                session=self._session,
                http_debug=self._http_debug
            )
            session_created = await self.session.create()

            if session_created is False:
                self.access_token_expiry = None
                _LOGGER.error("Error creating session")

            return access_token_updated and session_created
        except MfaRequired:
            raise
        except AuthError as exception:
            _LOGGER.error("Error updating access token. %s", exception)
            raise exception
        except SessionError as exception:
            self.access_token_expiry = None
            _LOGGER.error("Error creating session. %s", exception)
            raise exception

    async def __update_access_token(self, refresh: bool = False) -> bool:
        return_value = False
        id_token_response = 'idToken'
        refresh_token_response = 'refreshToken'
        expires_in_response = 'expiresIn'

        try:
            wrapper = APIWrapper(session=self._session)

            if refresh:
                _LOGGER.debug('Refreshing access token')
                headers = HEADERS.copy()
                headers["Content-type"] = 'application/x-www-form-urlencoded'

                url = f"{GOOGLE_TOKEN_BASE_URL}{TOKEN}"
                body = f"grant_type=refresh_token&refresh_token={self.refresh_token}"

                id_token_response = 'id_token'
                refresh_token_response = 'refresh_token'
                expires_in_response = 'expires_in'
            else:
                _LOGGER.debug('Getting a new access token')

                url = f"{GOOGLE_BASE_URL}{PASSWORD_VERIFY}"
                body = {"email": self.email, "returnSecureToken": True, "password": self.password}
                headers = HEADERS.copy()

            response = await wrapper.post(
                url=url,
                body=body,
                headers=headers,
                exception_class=AuthError)

            if response.status != 200:
                await self.__handle_response_error(response, AuthError)

            json = await response.json()
            if not refresh and json.get("mfaPendingCredential"):
                self._prepare_mfa(json)
                raise MfaRequired()
            access_token = json[id_token_response]
            refresh_token = json[refresh_token_response]
            expiry = datetime.now() + timedelta(
                seconds=int(json[expires_in_response]) - 10
            )
            self.access_token = access_token
            if refresh_token != self.refresh_token:
                self.refresh_token = refresh_token
                if self._on_refresh_token is not None:
                    self._on_refresh_token(refresh_token)
            self.access_token_expiry = expiry
            return_value = True

            if self._http_debug:
                _LOGGER.debug("Received authentication token response")
        except AuthError as exception:
            raise exception
        except KeyError as exception:
            raise AuthError(
                response.status,
                f"Error processing access token response. {exception} not found in json."
            ) from exception
        except (TypeError, ValueError) as exception:
            raise AuthError(
                response.status,
                f"Error processing access token response. \
When calculating expiry date, got: {exception}."
            ) from exception
        except APIError as exception:
            raise exception

        return return_value

    def _prepare_mfa(self, response: dict) -> None:
        self._mfa_pending_credential = None
        self._mfa_enrollment_id = None
        self._mfa_session_info = None
        phone_factors = [
            factor["mfaEnrollmentId"]
            for factor in response.get("mfaInfo", [])
            if factor.get("phoneInfo") and factor.get("mfaEnrollmentId")
        ]
        if len(phone_factors) != 1:
            raise MfaError(200, "Expected exactly one enrolled SMS factor")
        self._mfa_enrollment_id = phone_factors[0]
        self._mfa_pending_credential = response["mfaPendingCredential"]

    async def async_start_mfa(self) -> None:
        """Request an SMS code after password sign-in raises MfaRequired."""
        if not self._mfa_pending_credential:
            raise MfaError(400, "No pending two-step verification")
        self._mfa_session_info = None
        response = await self._mfa_request(MFA_START, {
            "mfaPendingCredential": self._mfa_pending_credential,
            "mfaEnrollmentId": self._mfa_enrollment_id,
            "phoneSignInInfo": {},
        })
        self._mfa_session_info = response.get("phoneResponseInfo", {}).get("sessionInfo")
        if not self._mfa_session_info:
            raise MfaError(200, "Missing SMS session")

    async def async_complete_mfa(self, code: str) -> bool:
        """Verify the SMS code and create the Pod Point session."""
        if not self._mfa_session_info:
            raise MfaError(400, "No active SMS challenge")
        response = await self._mfa_request(MFA_FINALIZE, {
            "mfaPendingCredential": self._mfa_pending_credential,
            "mfaEnrollmentId": self._mfa_enrollment_id,
            "phoneVerificationInfo": {"sessionInfo": self._mfa_session_info, "code": code},
        })
        self._mfa_pending_credential = None
        self._mfa_enrollment_id = None
        self._mfa_session_info = None
        if not response.get("refreshToken"):
            raise MfaError(200, "Missing refresh token after verification")
        # Finalize does not return an expiry. Exchange the refresh token to
        # obtain the usual access token, expiry and Pod Point session.
        self.refresh_token = response["refreshToken"]
        return await self.async_update_access_token()

    async def _mfa_request(self, url: str, body: dict) -> dict:
        # MFA request and response bodies contain one-time credentials.
        try:
            async with self._session.post(
                url, json=body, timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                try:
                    payload = await response.json()
                except ValueError:
                    raise MfaError(response.status, "Invalid verification response") from None
                if not isinstance(payload, dict):
                    raise MfaError(response.status, "Invalid verification response")
                if response.status != 200:
                    if payload.get("error", {}).get("message") == "INVALID_CODE":
                        raise MfaInvalidCode(response.status, "Incorrect verification code")
                    raise MfaError(response.status, "Verification request failed")
                return payload
        except (aiohttp.ClientError, asyncio.TimeoutError):
            raise MfaError(0, "Could not contact the verification service") from None

    async def __handle_response_error(self, response, error_class):
        status = response.status
        response = await response.text()

        if self._http_debug:
            _LOGGER.debug(response)

        raise error_class(status, response)
