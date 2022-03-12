from datetime import datetime
from dataclasses import dataclass
from re import M
from typing import Dict, Any

class Charge:
    def __init__(self, data: Dict[str, Any]):
        self.id: int             = data.get('id', None)
        self.kwh_used: float     = data.get('kwh_used', 0.0)
        self.duration: int       = data.get('duration', 0)
        self.starts_at: datetime = data.get('starts_at', None)
        self.ends_at: datetime   = data.get('ends_at', None)
        self.energy_cost: int    = data.get('energy_cost', None)

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


    @dataclass
    class BillingEvent:
        id: int                   = None
        amount: Any               = None
        currency: Any             = None
        exchange_rate: int        = 0
        presentment_amount: Any   = None
        presentment_currency: Any = None


    class Location:
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
            id: int            = None
            business_name: str = ""


    @dataclass
    class Pod:
        id: int = None

    @dataclass
    class Organisation:
        id: int   = None
        name: str = None
