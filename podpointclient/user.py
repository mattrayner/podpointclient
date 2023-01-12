"""Charge class, represents a 'Charge' from the podpoint apis"""

from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass, field
from .helpers.functions import lazy_convert_to_datetime
from .pod import Pod
import json

@dataclass
class Address:
    business_name: str
    address1: str
    address2: str
    town: str
    postcode: str
    country: str

    @property
    def dict(self):
        return {
            "business_name": self.business_name,
            "address1": self.address1,
            "address2": self.address2,
            "town": self.town,
            "postcode": self.postcode,
            "country": self.country
        }

@dataclass
class Image:
    half_size: str
    seventy_five_percent: str
    original: str

    @property
    def dict(self):
        return {
            "@1x": self.half_size,
            "@2x": self.seventy_five_percent,
            "@3x": self.original
        }

@dataclass
class VehicleMake:
    id: int
    name: str
    logo: Image

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "logo": self.logo.dict
        }

@dataclass
class Vehicle:
    id: int
    uuid: str
    name: str
    capacity: int
    batteryCapacity: float
    startYear: int
    endYear: int
    image: Image
    make: VehicleMake

    @property
    def dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "capacity": self.capacity,
            "batteryCapacity": self.batteryCapacity,
            "startYear": self.startYear,
            "endYear": self.endYear,
            "image": self.image.dict,
            "make": self.make.dict
        }

@dataclass
class Unit:
    id: int
    ppid: str
    name: str
    status: str
    architecture: str
    pod: Pod

    @property
    def dict(self):
        return {
            "id": self.id,
            "ppid": self.ppid,
            "name": self.name,
            "status": self.status,
            "architecture": self.architecture,
            "pod": self.pod.dict
        }

class User:
    """Representation of a User from pod point"""
    def __init__(self, data: Dict[str, Any]):
        self.id: int             = data.get('id', None)
        self.email: str          = data.get('email', None)
        self.first_name: str     = data.get('first_name', None)
        self.last_name: str      = data.get('last_name', None)
        self.role: str           = data.get('role', None)
        self.hasHomeCharge: int  = data.get('hasHomeCharge', 0)
        self.locale: str         = data.get('locale', None)
        self.preferences: List[self.UserPreferences] = []

        for preference_data in data.get('preferences', []):
            self.preferences.append(self.UserPreference(unitOfDistance=preference_data.get('unitOfDistance')))

        self.account: self.UserAccount = None
        account_data = data.get('account', {})
        if account_data:
            billing_address_data = account_data.get('billing_address', {})
            billing_address = Address(
                business_name = billing_address_data.get('business_name', None),
                address1 = billing_address_data.get('address1', None),
                address2 = billing_address_data.get('address2', None),
                town = billing_address_data.get('town', None),
                postcode = billing_address_data.get('postcode', None),
                country = billing_address_data.get('country', None)
            )

            self.account = self.UserAccount(
                user_id = account_data.get('user_id', None),
                uid = account_data.get('uid', None),
                balance = account_data.get('balance', None),
                currency = account_data.get('currency', None),
                phone = account_data.get('phone', None),
                mobile = account_data.get('mobile', None),
                billing_address = billing_address
            )

        self.vehicle: Vehicle = None
        vehicle_data = data.get('vehicle', {})
        if vehicle_data:
            image_data = vehicle_data.get('image', {})
            image = Image(
                half_size = image_data.get("@1x", None),
                seventy_five_percent = image_data.get("@2x", None),
                original = image_data.get("@3x", None)
            ) if image_data else None

            make_data = vehicle_data.get('make', {})
            make_logo_data = make_data.get('logo', {})
            make_logo = Image(
                half_size = make_logo_data.get('@1x', None),
                seventy_five_percent = make_logo_data.get('@2x', None),
                original = make_logo_data.get('@3x', None)
            ) 
            make = VehicleMake(
                id = make_data.get('id', None),
                name = make_data.get('name', None),
                logo = make_logo
            )

            self.vehicle = Vehicle(
                    id = vehicle_data.get('id', None),
                    uuid = vehicle_data.get('uuid', None),
                    name = vehicle_data.get('name', None),
                    capacity = vehicle_data.get('capacity', 0),
                    batteryCapacity = vehicle_data.get('batteryCapacity', 0.0),
                    startYear = vehicle_data.get('startYear', 0),
                    endYear = vehicle_data.get('startYear', 0),
                    image = image,
                    make = make
            )

        self.unit: Unit = None
        unit_data = data.get('unit', {})
        if unit_data:
            self.unit = Unit(
                id = unit_data.get('id', None),
                ppid = unit_data.get('ppid', None),
                name = unit_data.get('name', None),
                status = unit_data.get('status', None),
                architecture = unit_data.get('architecture', None),
                pod = Pod(data=unit_data.get('pod', {}))
            )

    @property
    def dict(self):
        preferences_list = []
        for preference in self.preferences:
            preferences_list.append(
                preference.dict
            )

        dict = {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "hasHomeCharge": self.hasHomeCharge,
            "locale": self.locale,
            "preferences": preferences_list,
        }

        if self.account:
            dict["account"] = self.account.dict

        if self.vehicle:
            dict["vehicle"] = self.vehicle.dict

        if self.unit:
            dict["unit"] = self.unit.dict

        return dict

    def to_json(self):
        """JSON representation of a User object"""
        return json.dumps(self.dict, ensure_ascii=False)

    @dataclass
    class UserPreference:
        unitOfDistance: str

        @property
        def dict(self):
            return {
                "unitOfDistance": self.unitOfDistance
            }

    @dataclass
    class UserAccount:
        user_id: int
        uid: str
        balance: int
        currency: str

        billing_address: Address

        phone: str
        mobile: str

        @property
        def dict(self):
            return {
                "user_id": self.user_id,
                "uid": self.uid,
                "balance": self.balance,
                "currency": self.currency,
                "billing_address": self.billing_address.dict,
                "phone": self.phone,
                "mobile": self.mobile
            }
