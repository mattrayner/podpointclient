"""Charge class, represents a 'Charge' from the podpoint apis"""

from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass, field
from .helpers.functions import lazy_convert_to_datetime

@dataclass
class ChargeDurationFormat:
    """Representation of Format within Duration within Charge from pod point"""
    value: str = None
    unit: str  = None

    def __str__(self) -> str:
        return " ".join(list(filter(None, [self.value, self.unit])))


class Charge:
    """Representation of a Charge from pod point"""
    def __init__(self, data: Dict[str, Any]):
        self.id: int             = data.get('id', None)
        self.kwh_used: float     = data.get('kwh_used', 0.0)
        self.duration: int       = data.get('duration', 0)
        self.starts_at: datetime = lazy_convert_to_datetime(data.get('starts_at', None))
        self.ends_at: datetime   = lazy_convert_to_datetime(data.get('ends_at', None))
        self.energy_cost: int    = data.get('energy_cost', 0)

        charging_duration_data = data.get('charging_duration', {})
        self.charging_duration = self.ChargingDuration(
            raw       = charging_duration_data.get('raw', None),
            formatted = charging_duration_data.get('formatted', [])
        )

        billing_event_data = data.get('billing_event', {})
        self.billing_event = self.BillingEvent(
            id                   = billing_event_data.get('id', None),
            amount               = billing_event_data.get('amount', None),
            currency             = billing_event_data.get('currency', None),
            exchange_rate        = billing_event_data.get('exchange_rate', 0),
            presentment_amount   = billing_event_data.get('presentment_amount', None),
            presentment_currency = billing_event_data.get('presentment_currency', None)
        )

        location_data = data.get('location', {})
        self.location = self.Location(data=location_data)

        pod_data = data.get('pod', {})
        self.pod = self.Pod(id=pod_data.get('id', None))

        organisation_data = data.get('organisation', {})
        self.organisation = self.Organisation(
            id = organisation_data.get('id', None),
            name = organisation_data.get('name', None)
        )

    @property
    def home(self) -> bool:
        """Is this a 'home' charge?"""
        return self.location.home


    @dataclass
    class ChargingDuration:
        """Representation of a Duration within a Charge from pod point"""
        raw: int                                = None
        formatted: 'list[ChargeDurationFormat]' = field(default_factory=list)

        def __init__(self, raw: int, formatted: List[Dict[str,str]]) -> None:
            self.raw = raw
            self.formatted: List[ChargeDurationFormat] = []

            if formatted is not None and len(formatted) > 0:
                for formatted_data in formatted:
                    self.formatted.append(
                        ChargeDurationFormat(
                            value = formatted_data.get("value", None),
                            unit  = formatted_data.get("unit", None)
                        )
                    )

        def __str__(self) -> str:
            def dt_to_str(date_time: datetime) -> str:
                return str(date_time)

            return " ".join(list(filter(None, map(dt_to_str ,self.formatted))))


    @dataclass
    class BillingEvent:
        """Represents a Billing Event from pod point"""
        id: int                   = None
        amount: Any               = None
        currency: Any             = None
        exchange_rate: int        = 0
        presentment_amount: Any   = None
        presentment_currency: Any = None


    @dataclass
    class Location:
        """Represents a Location within a charge from pod point"""
        def __init__(self, data: Dict[str, Any]):
            self.id       = data.get('id', None)
            self.home     = data.get('home', None)
            self.timezone = data.get('timezone', None)

            address_data = data.get('address', {})
            self.address = self.Address(
                id=address_data.get('id', None),
                business_name=address_data.get('business_name', "")
            )


        @dataclass
        class Address:
            """Represents an address within a Location within a Charge from Pod Point"""
            id: int            = None
            business_name: str = ""


    @dataclass
    class Pod:
        """Represents a Pod within a Charge from pod point"""
        id: int = None

    @dataclass
    class Organisation:
        """Repreents an Organisation within a Charge from pod point"""
        id: int   = None
        name: str = None
