# Pod Point Client

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Unofficial API client for [Pod Point][pod_point_web] with a focus on home users._


## Installation

```bash
pip install podpointclient
```

## Usage

The [Pod Point Client][pod_point_client] supports the following methods:

Method | Description
---|---
`async_get_pods()` | *Get all pods from a user's account* - Returns a list of `Pod` objects.
`async_get_pod(pod_id=1234)` | *Gets an individual pod* - Returns a single `Pod`. *_NOTE: The Pod Point API does not support a single-pod return so this method gets all pods and filters._*
`async_set_schedule(enabled=False, pod=pod)` | *Updates a pod with a week of schedules that will enable or disable charging* - See setting charging schedules for more information on how this works.

### Example

The below walks through a common scenario: 

1. Get all pods
1. Updating the schedule of an individual pod
1. Confirm that it worked

> `PodPointClient` is async by default so the below example assumes you are running it within an async function.

```python
from podpointclient import PodPointClient

# Create a client
client = PodPointClient(username="test@example.com", password="passw0rd!1")

# Get all pods for a user
pods = await client.async_get_pods()

# Select one to update schedules for
pod = pods[0]

# Update schedule to disabled (allow charging at any time)
await client.async_set_schedule(enabled=False, pod=pod)

# Get just that pod
pod = await client.async_get_pod(pod_id=pod.id)
# Check if the schedule is disabled
schedule_status = pod.charge_schedules[0].is_active
print(schedule_status)
```

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md).

[pod_point_web]: https://pod-point.com
[pod_point_client]: https://github.com/mattrayner/podpointclient
[buymecoffee]: https://www.buymeacoffee.com/mattrayner
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/mattrayner/podpointclient.svg?style=for-the-badge
[commits]: https://github.com/mattrayner/podpointclient/commits/master
[license-shield]: https://img.shields.io/github/license/mattrayner/podpointclient.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Matt%20Rayner-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/mattrayner/podpointclientt.svg?style=for-the-badge
[releases]: https://github.com/mattrayner/podpointclient/releases
