"""Sample API Client."""
import logging
from typing import Dict, Any, List
from datetime import datetime

import aiohttp

from podpointclient.schedule import Schedule

from .endpoints import API_BASE_URL, CHARGE_SCHEDULES, PODS, UNITS, USERS, CHARGES
from .helpers.auth import Auth
from .helpers.functions import auth_headers
from .helpers.api_wrapper import APIWrapper
from .factories import PodFactory, ScheduleFactory, ChargeFactory
from .pod import Pod

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class PodPointClient:
    """API Client for communicating with Pod Point."""

    def __init__(
        self,   
        username: str,
        password: str,
        session: aiohttp.ClientSession = aiohttp.ClientSession(),
        include_timestamp: bool = False,
        http_debug: bool = None
    ) -> None:
        """Pod Point API Client."""
        self.email = username
        self.password = password
        self._session = session
        self._http_debug = http_debug if http_debug is not None else False
        self.auth = Auth(
            email=self.email,
            password=self.password,
            session=self._session,
            http_debug=self._http_debug
        )
        self.api_wrapper = APIWrapper(session=self._session)
        self.include_timestamp = include_timestamp

    async def async_get_pods(self) -> List[Pod]:
        """Get pods from the API."""
        await self.auth.async_update_access_token()

        path = f"{USERS}/{self.auth.user_id}{PODS}"
        url = f"{API_BASE_URL}{path}"

        includes = ["statuses", "price", "model", "unit_connectors", "charge_schedules"]
        params = {"perpage": "all", "include": ",".join(includes)}
        if self.include_timestamp:
            params = self._add_timestamp_to_params(params)

        headers = auth_headers(access_token=self.auth.access_token)

        response = await self.api_wrapper.get(url=url, params=params, headers=headers)

        json = await response.json()

        if self._http_debug:
            _LOGGER.debug(json)

        factory = PodFactory()
        pods = factory.build_pods(pods_response=json)

        return pods

    async def async_get_pod(self, pod_id: int) -> Pod:
        """Get specific pod from the API."""
        pods = await self.async_get_pods()
        return next((pod for pod in pods if pod.id == pod_id), None)

    async def async_set_schedule(self, enabled: bool, pod: Pod) -> bool:
        """Send data from the API."""
        await self.auth.async_update_access_token()

        unit_id = pod.unit_id

        _LOGGER.debug(
            "Updating pod schedule for unit %s. Enabling schedule: %s",
            unit_id,
            enabled
        )

        path = f"{UNITS}/{unit_id}{CHARGE_SCHEDULES}"
        url = f"{API_BASE_URL}{path}"
        params = None
        if self.include_timestamp:
            params = self._add_timestamp_to_params({})

        headers = auth_headers(access_token=self.auth.access_token)
        payload = self._schedule_data(enabled=enabled)

        response = await self.api_wrapper.put(url=url, body=payload, headers=headers, params=params)

        if response.status == 201:
            return True

        text = await response.text()
        _LOGGER.warning(
            "Expected to recieve 201 status code when creating schedules. Got (%s) - %s",
            response.status,
            text
        )
        return False

    async def async_get_charges(self, per_page: str = "5", page: str = "1"):
        """Get charges from the API."""
        await self.auth.async_update_access_token()

        path = f"{USERS}/{self.auth.user_id}{CHARGES}"
        url = f"{API_BASE_URL}{path}"
        params = {"perpage": per_page, "page": page}
        if self.include_timestamp:
            params = self._add_timestamp_to_params(params)

        headers = auth_headers(access_token=self.auth.access_token)

        response = await self.api_wrapper.get(url=url, params=params, headers=headers)

        json = await response.json()

        if self._http_debug:
            _LOGGER.debug(json)

        factory = ChargeFactory()
        charges = factory.build_charges(charge_response=json)

        return charges

    def _schedule_data(self, enabled: bool) -> Dict[str, Any]:
        factory = ScheduleFactory()
        schedules: List[Schedule] = factory.build_schedules(enabled=enabled)

        d_list = list(map(lambda schedule: schedule.dict, schedules))

        return {"data": d_list}

    def _add_timestamp_to_params(self, params: Dict[str, Any]) -> Dict[str, any]:
        params["timestamp"] = datetime.now().timestamp()

        return params
