from datetime import datetime, timedelta
from podpointclient.client import PodPointClient
import asyncio
import aiohttp


async def main(username: str, password: str, http_debug: bool = False, loop=None):
    # Create a session
    session = aiohttp.ClientSession(loop=loop)

    print(f"Logging into Pod Point with email: {username}")

    # Create a client
    client = PodPointClient(
        username=username,
        password=password,
        session=session,
        http_debug=http_debug
    )

    # Verify credentials work
    verified = await client.async_credentials_verified()
    print(f"Credentials verified: {verified}")
    print(f"  Token expiry: {client.auth.access_token_expiry}")

    print("Sleeping 2s")
    time.sleep(2)

    # Get user information
    print("Getting user details")
    user = await client.async_get_user()
    print(f"  Account balance {user.account.balance}p")

    print("Getting pods")
    # Get all pods for a user
    pods = await client.async_get_all_pods()
    print(f"  Found {len(pods)} pod(s).")

    # Select one to update schedules for
    pod = pods[0]
    print(f"Selecting first pod: {pod.ppid}")

    # Get firmware information for the pod
    firmwares = await client.async_get_firmware(pod=pod)
    firmware = firmwares[0]
    print(f"Gettnig firmware data for {pod.ppid}")
    print(f"  Serial: {firmware.serial_number}")
    print(f"  Update available: {firmware.update_available}")

    print(f"Enabling charging for {pod.ppid}")
    # Update schedule to disabled (allow charging at any time)
    await client.async_set_schedule(enabled=False, pod=pod)

    # Get just that pod
    pod = await client.async_get_pod(pod_id=pod.id)
    # Check if the schedule is disabled
    schedule_status = pod.charge_schedules[0].is_active
    print(f"  Schedule active: {schedule_status}")

    # Print last charge energy use
    print(f"Getting last charge for pod {pod.ppid}")
    charges = await client.async_get_charges(perpage=1, page=1)
    energy_used = charges[0].kwh_used
    print(f"  kW charged: {energy_used}")

    # Expire token and exchange a refresh
    print("Expiring token and refreshing...")
    client.auth.access_token_expiry = datetime.now() - timedelta(minutes=10)
    updated = await client.auth.async_update_access_token()
    print(f"  Token updated? {updated} - New expiry: {client.auth.access_token_expiry}")

    # Get user information again
    print("Getting user details with new token")
    user = await client.async_get_user()
    print(f"  Account balance {user.account.balance}p")

if __name__ == "__main__":
    import time
    import argparse

    parser = argparse.ArgumentParser(description="Run the example provided in the Readme to verify functionality.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--email", type=str, help="Pod Point email")
    parser.add_argument("-p", "--password", type=str, help="Pod Point password")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable HTTP debugging")
    args = parser.parse_args()
    config = vars(args)

    print("-- Pod Point client test script --")

    start = time.perf_counter()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(
            username=config['email'],
            password=config['password'],
            http_debug=config['debug'],
            loop=loop
        )
    )
    loop.close()

    print("")
    elapsed = time.perf_counter() - start
    print(f"Script executed in {elapsed:0.2f} seconds")
