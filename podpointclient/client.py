"""PodPoint Basic API Client."""
import logging
from typing import Dict, Any, List, Union
from datetime import datetime

import aiohttp

from .endpoints import API_BASE_URL, CHARGE_SCHEDULES, PODS, UNITS, USERS, CHARGES, FIRMWARE
from .helpers.auth import Auth
from .helpers.functions import auth_headers
from .helpers.api_wrapper import APIWrapper
from .factories import PodFactory, ScheduleFactory, ChargeFactory, FirmwareFactory
from .pod import Pod, Firmware
from .charge import Charge
from .schedule import Schedule

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}
DEFAULT_INCLUDES = ["statuses", "price", "model",
                    "unit_connectors", "charge_schedules"]


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

    async def async_credentials_verified(self) -> bool:
        """Perform a minimum call to verify we have working credentials and can get one Pod"""
        await self.auth.async_update_access_token()

        pods = await self.async_get_pods(perpage=1, page=1, includes=[])
        return len(pods) > 0

    async def async_get_all_pods(
        self,
        perpage: Union[str, int] = 5,
        includes: Union[List[str], None] = None
    ) -> List[Pod]:
        """Get all pods from the API"""
        page = 1
        pods: List[Pod] = []

        more_pods = True
        while more_pods:
            new_pods: List[Pod] = await self.async_get_pods(
                perpage=perpage,
                page=page,
                includes=includes
            )
            # Should be replaced by reading "meta > pagination > page_count" but
            # would require a larger refactor
            if len(new_pods) < perpage:
                more_pods = False

            pods.extend(new_pods)
            page += 1

        return pods

    async def async_get_pods(
        self,
        perpage: Union[str, int] = 5,
        page: Union[str, int] = 1,
        includes: Union[List[str], None] = None
    ) -> List[Pod]:
        """Get pods from the API"""
        await self.auth.async_update_access_token()

        if includes is None:
            includes = DEFAULT_INCLUDES

        params = {"perpage": perpage, "page": page}
        if len(includes) > 0:
            params["include"] = ",".join(includes)

        response = await self.api_wrapper.get(
            url=self._url_from_path(path=f"{USERS}/{self.auth.user_id}{PODS}"),
            params=self._generate_complete_params(params=params),
            headers=auth_headers(access_token=self.auth.access_token)
        )

        json = await self._handle_json_response(response=response)

        pods = PodFactory().build_pods(pods_response=json)

        return pods

    async def async_get_pod(self, pod_id: int) -> Pod:
        """Get specific pod from the API"""
        pods = await self.async_get_all_pods()
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

        response = await self.api_wrapper.put(
            url=self._url_from_path(
                path=f"{UNITS}/{unit_id}{CHARGE_SCHEDULES}"),
            params=self._generate_complete_params(params=None),
            headers=auth_headers(access_token=self.auth.access_token),
            body=self._schedule_data(enabled=enabled)
        )

        #  Quick exit if the response code is 201
        if response.status == 201:
            return True

        text = await response.text()
        _LOGGER.warning(
            "Expected to recieve 201 status code when creating schedules. Got (%s) - %s",
            response.status,
            text
        )
        return False

    async def async_get_all_charges(
        self,
        perpage: Union[str, int] = 50
    ) -> List[Charge]:
        """Get all charges from the API"""
        page = 1
        charges: List[Charge] = []

        more_charges = True
        while more_charges:
            new_charges: List[Charge] = await self.async_get_charges(perpage=perpage, page=page)
            # Should be replaced by reading "meta > pagination > page_count" but
            # would require a larger refactor
            if len(new_charges) < perpage:
                more_charges = False

            charges.extend(new_charges)
            page += 1

        return charges

    async def async_get_charges(
        self,
        perpage: Union[str, int] = 5,
        page: Union[str, int] = 1
    ) -> List[Charge]:
        """Get charges from the API."""
        await self.auth.async_update_access_token()

        response = await self.api_wrapper.get(
            url=self._url_from_path(
                path=f"{USERS}/{self.auth.user_id}{CHARGES}"),
            params=self._generate_complete_params(
                params={"perpage": perpage, "page": page}),
            headers=auth_headers(access_token=self.auth.access_token)
        )

        json = await self._handle_json_response(response=response)

        charges = ChargeFactory().build_charges(charge_response=json)

        return charges

    async def async_get_firmware(self, pod: Pod) -> List[Firmware]:
        """Get firmware information for a given unit."""
        await self.auth.async_update_access_token()
        
        response = await self.api_wrapper.get(
            url=self._url_from_path(
                path=f"{UNITS}/{pod.unit_id}{FIRMWARE}"),
            params=self._generate_complete_params(params=None),
            headers=auth_headers(access_token=self.auth.access_token)
        )

        json = await self._handle_json_response(response=response)

        firmwares = FirmwareFactory().build_firmwares(firmware_response=json)

        return firmwares


    def _schedule_data(self, enabled: bool) -> Dict[str, Any]:
        """Generate a new schedule body with all the enable attributes set to the `enabled` value"""
        schedules: List[Schedule] = ScheduleFactory(
        ).build_schedules(enabled=enabled)

        d_list = list(map(lambda schedule: schedule.dict, schedules))

        return {"data": d_list}

    def _url_from_path(self, path: str) -> str:
        """Given a path, return a complete API URL"""
        return f"{API_BASE_URL}{path}"

    def _generate_complete_params(self, params: Union[None, Dict[str, Any]]) -> Dict[str, any]:
        """Given a params object, add optional params if required"""
        if not self.include_timestamp:
            return params

        if params is None:
            params = {}

        params["timestamp"] = datetime.now().timestamp()
        return params

    async def _handle_json_response(self, response: aiohttp.ClientResponse) -> Dict[str, any]:
        """Given a Coroutine (assuming a response from ApiWrapper), await calling
        json() and if needed, debug log the response"""
        json = await response.json()

        if self._http_debug:
            _LOGGER.debug(json)

        return json
