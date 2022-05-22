# Pod Point Client Changelog

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