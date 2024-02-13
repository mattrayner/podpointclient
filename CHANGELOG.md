# Pod Point Client Changelog

## v1.5.0

* Add support for refreshing expired tokens, rather than grabbing new ones each time
* Update example.py to demonstrate token expiry

## v1.4.3

* Remove additional / from pod point api calls

## v1.4.2

* Fix an issue with `Session` inside of `Auth` causing token re-authentication to fail

## v1.4.1

* Add additional debug logs for testing new google auth

## v1.4.0

* Update auth system to new Google-based auth from Pod Point

## v1.3.1

* Add `pytz` as a dependency
* Fix `Pod.charge_mode` bug

## v1.3.0

* Migrate to API v5 - @mattrayner
* Add support for charge overrides:
  * Add `ChargeMode` enum - @mattrayner
  * Add `ChargeOverride` - @mattrayner
  * Add `Client.async_get_charge_override` - @mattrayner
  * Add `Client.async_set_charge_override` - @mattrayner
  * Add `Client.async_set_charge_mode_manual` - @mattrayner
  * Add `Client.async_set_charge_mode_smart` - @mattrayner
  * Add `Pod.charge_override` - @mattrayner
  * Add `Pod.charge_mode` - @mattrayner
* Add api wrapper delete support

## v1.2.0

* Add `User` - @mattrayner
* Add `Client.async_get_user_info` - @mattrayner

## v1.1.0

* Add `Firmware` to `Pod` - @mattrayner
* Add `Client.async_get_firmware` call - @mattrayner

## v1.0.0

* Add lightweight credential verification call - @mattrayner
* Add support for pagination rather than just adding 'perpage=all' - @mattrayner
* Updated README with new instructions - @mattrayner
* Fixed GitHub Actions - @mattrayner
  * Added code coverage artifacts, so you can download the cov report for a run
* Refactored code to improve dryness - @mattrayner
* Added additional testing dependencies - @mattrayner
* Add CD pipeline, when a new tag/release is pushed, auto-publish to PyPi - @mattrayner

## v0.3.0

* Add http_debug flag - @mattrayner
* When enabled, complete response bodies will be sent to logger.debug
* Restructured helpers and other classes so that they made more sense - @mattrayner
* Completed a pylon pass to standardize the code base - @mattrayner
* Improved test coverage - @mattrayner

## v0.2.2

* Make timestamp=XXX optional, and off by default
* Greatly improve test coverage

## v0.2.1

* Add charge duration seconds to Charge allowing for more granular tracking of charging time

## v0.2.0

* Add `ChargeDuration` to `Charge` as `charge.charge_duration`
  * Charge duration is the amount of time during a charge 'session' spent delivering power. Available as `raw` int duration and as `formatted` value e.g. '1 hour 32 minutes', '<5 minutes', '2 hours 5 minutes' etc.
  * String-ing a ChargeDuration returns the formatted string and Int-ing a ChargeDuration returns the raw value

## v0.1.3

* Stop supressing `AuthError` and `SessionError`. This allows upstream clients to correctly handle these.

## v0.1.2

* Add placeholder values for pods:
  * `.total_kwh`
  * `.current_kwh`
  * `.charges`

## v0.1.1

* Add `.home` attribute to `Pod` objects

## v0.1.0

* Add 'Charges' functionality
* Update README

## v0.0.9

* Fix issues with imports and testing

## v0.0.1

* Initial client with basic functionality for Home Assistant component
  * Get all user pods
  * Update schedules

* Created initial mapping classes:
  * Pod
  * Schedule
  * Charge

* Added initial base test coverage

* Setup initial README

* Added MIT License

* Created CHANGELOG
