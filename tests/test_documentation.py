from podpointclient.client import PodPointClient
import aiohttp
from aioresponses import aioresponses

from podpointclient.pod import Pod, Firmware
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

            # Verify credentials work
            verified = await client.async_credentials_verified()
            print(verified)
            assert verified is True

            # Get user information
            user = await client.async_get_user()
            print(f"Account balance {user.account.balance}p")
            assert user.account.balance == 173

            # Get all pods for a user
            pods = await client.async_get_all_pods()
            assert len(pods) == 1
            
            # Select one to update schedules for
            pod = pods[0]
            assert isinstance(pod, Pod) is True

            # Get firmware information for the pod
            firmwares = await client.async_get_firmware(pod=pod)
            firmware = firmwares[0]
            assert isinstance(firmware, Firmware)
            print(firmware.serial_number)
            assert firmware.serial_number == '123456789'
            print(firmware.update_available)
            assert firmware.update_available is False

            # Update schedule to disabled (allow charging at any time)
            success = await client.async_set_schedule(enabled=False, pod=pod)
            assert success is True

            # Get just that pod
            pod = await client.async_get_pod(pod_id=pod.id)
            # Check if the schedule is disabled
            schedule_status = pod.charge_schedules[0].is_active
            print(schedule_status)
            assert schedule_status is False

            # Print last charge energy use
            charges = await client.async_get_charges(perpage=1, page=1)
            energy_used = charges[0].kwh_used
            print(energy_used)
            assert energy_used == 12.2
