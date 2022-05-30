from podpointclient.client import PodPointClient
import aiohttp
from aioresponses import aioresponses

from podpointclient.pod import Pod
from helpers import Mocks

from freezegun import freeze_time

@freeze_time("Jan 1st, 2022")
async def test_readme():
    with aioresponses() as m:
        mocks = Mocks(m)
        mocks.happy_path()

        async with aiohttp.ClientSession() as session:
            # Create a client
            client = PodPointClient(username="test@example.com", password="passw0rd!1", session=session)

            # Get all pods for a user
            pods = await client.async_get_pods()
            assert len(pods) == 1
            
            # Select one to update schedules for
            pod = pods[0]
            assert type(pod) is Pod

            # Update schedule to disabled (allow charging at any time)
            success = await client.async_set_schedule(enabled=False, pod=pod)
            assert success is True

            # Get just that pod
            pod = await client.async_get_pod(pod_id=pod.id)
            # Check if the schedule is disabled
            schedule_status = pod.charge_schedules[0].is_active
            print(schedule_status)
            assert schedule_status is False
