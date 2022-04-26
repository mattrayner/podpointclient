"""Sample API Client."""
import logging
from typing import Optional, Dict, Any, List
import aiohttp
from datetime import datetime, timedelta

from podpointclient.schedule import Schedule

from .endpoints import API_BASE_URL, CHARGE_SCHEDULES, PODS, UNITS, USERS, CHARGES
from .helpers.auth import Auth
from .helpers.helpers import APIWrapper, Helpers
from .factories import PodFactory, ScheduleFactory, ChargeFactory
from .pod import Pod

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class PodPointClient:
    """API Client for communicating with Pod Point."""

    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession = aiohttp.ClientSession()
    ) -> None:
        """Pod Point API Client."""
        self.email = username
        self.password = password
        self._session = session
        self.auth = Auth(
            email=self.email, 
            password=self.password, 
            session=self._session
        )
        self.api_wrapper = APIWrapper(session=self._session)

    async def async_get_pods(self) -> List[Pod]:
        """Get pods from the API."""
        await self.auth.async_update_access_token()

        path = f"{USERS}/{self.auth.user_id}{PODS}"
        url = f"{API_BASE_URL}{path}"

        includes = ["statuses", "price", "model", "unit_connectors", "charge_schedules"]
        params = {"perpage": "all", "include": ",".join(includes)}

        helpers = Helpers()
        headers = helpers.auth_headers(access_token=self.auth.access_token)

        response = await self.api_wrapper.get(url=url, params=params, headers=headers)

        json = await response.json()

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

        _LOGGER.info(
            f"Updating pod schedule for unit {unit_id}. Enabling schedule: {enabled}"
        )
        
        path = f"{UNITS}/{unit_id}{CHARGE_SCHEDULES}"
        url = f"{API_BASE_URL}{path}"

        helpers = Helpers()
        headers = helpers.auth_headers(access_token=self.auth.access_token)
        payload = self._schedule_data(enabled=enabled)

        _LOGGER.debug(f"Schedule payload: %s", payload)

        response = await self.api_wrapper.put(url=url, body=payload, headers=headers)

        if response.status == 201:
            _LOGGER.debug("Response: %s", await response.text())
            return True
        else:
            text = await response.text()
            _LOGGER.warn("Expected to recieve 201 status code when creating schedules. Got (%s) - %s", response.status, text)
            return False

    async def async_get_charges(self, per_page: str = "5", page: str = "1"):
        """Get charges from the API."""
        await self.auth.async_update_access_token()

        path = f"{USERS}/{self.auth.user_id}{CHARGES}"
        url = f"{API_BASE_URL}{path}"
        params = {"perpage": per_page, "page": page}

        helpers = Helpers()
        headers = helpers.auth_headers(access_token=self.auth.access_token)

        response = await self.api_wrapper.get(url=url, params=params, headers=headers)

        json = await response.json()

        factory = ChargeFactory()
        charges = factory.build_charges(charge_response=json)

        return charges

    def _schedule_data(self, enabled: bool) -> Dict[str, Any]:
        factory = ScheduleFactory()
        schedules: List[Schedule] = factory.build_schedules(enabled=enabled)

        d_list = list(map(lambda schedule: schedule.dict, schedules))

        return {"data": d_list}
