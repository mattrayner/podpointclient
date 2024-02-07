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
`async_credentials_verified()` | *Verify that the credentials we have can pull _atleast_ one Pod* - Returns `bool`.
`async_get_all_pods(includes=[])` | *Get all pods from a user's account* - Returns a list of `Pod` objects. Optional `includes` can be used to change what will be returned. Defaults to all data.
`async_get_pods(perpage=5, page=2, includes=[])` | *Get pods from a user's account* - Returns a list of `Pod` objects. `perpage` can be 'all', or a number. Can get additional pages with `page` attribute. `includes` is a list of additional information pulled for the Pod. Pass an empty list to `includes` for minimal information or `None` for full data (defaults to `None`).
`async_get_pod(pod_id=1234)` | *Gets an individual pod* - Returns a single `Pod`. *_NOTE: The Pod Point API does not support a single-pod return so this method gets all pods and filters._*
`async_set_schedule(enabled=False, pod=pod)` | *Updates a pod with a week of schedules that will enable or disable charging* - See setting charging schedules for more information on how this works.
`async_get_all_charges()` | *Get all charges from a user's account* - Returns a list of `Charge` objects.
`async_get_charges(perpage=5, page=2)` | *Get charges for a user* - Returns a list of `Charge` objects. `perpage` can be 'all', or a number. Can get additional pages with `page` attribute.
`async_get_firmware(pod=_Pod_)` | *Get firmware information for a pod* - Returns a list of `Firmware` objects.
`async_get_user(includes=[])` | *Get current user account information* - Returns a `User` object including account balance, units and vehicles. `includes` is a list of additional information pulled for a User. Pass an empty list to `includes` for minimal information or `None` for full data (defaults to `None`)

### Example

Included in the project is `example.py` which walks through a common scenario: 

1. Get all pods
1. Get firmware and serial number data for one pod
1. Updating the schedule of an individual pod
1. Confirm that it worked
1. Get information from the last charge

> You must provide your email address and password to the script as detailed below:

```bash
python3 example.py --email PODPOINTEMAIL --password PODPOINTPASSWORD
```

### Setting charging schedules

> **NOTE:** According to Pod Point, schedules can take up to 5 minutes to be recognised by a device. This applies to both updating of a schedule affecting a device, and the device recognising that it is active/inactive due to entering/exiting a schedule window.

Currently this client supports setting the same schedule across all days for the week. By default it is designed to be used as an on/off switch for charging and creates a schedule lasting 1 second, from 00:00:00 - 00:00:01.

Due to the delay in pods recognising that they are in/out of a schedule this realistically means charging is turned off when this schedule is enabled.

You are able to pass a start_time and end_time when setting schedules but these are set for all days and are in-day only. By which I mean passing `start_time="18:00"` and `end_time="00:15"` will fail as `00:15` is before the start time.


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
[releases-shield]: https://img.shields.io/github/release/mattrayner/podpointclient.svg?style=for-the-badge
[releases]: https://github.com/mattrayner/podpointclient/releases
