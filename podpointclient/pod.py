from dataclasses import dataclass
from datetime import datetime
from sqlite3 import DatabaseError
from typing import Dict, Any
from .schedule import Schedule, ScheduleStatus
from enum import auto
from strenum import StrEnum, KebabCaseStrEnum
from .helpers.helpers import Helpers
import json


class StatusName(StrEnum):
    AVAILABLE      = "Available"
    UNAVAILABLE    = "Unavailable"
    CHARGING       = "Charging"
    OUT_OF_SERVICE = "Out of Service"


class StatusKeyName(KebabCaseStrEnum):
    AVAILABLE      = auto()
    UNAVAILABLE    = auto()
    CHARGING       = auto()
    OUT_OF_SERVICE = auto()


@dataclass
class Socket:
    type: str
    description: str
    ocpp_name: str
    ocpp_code: int

    @property
    def dict(self):
        return {
            "type": self.type,
            "description": self.description,
            "ocpp_name": self.ocpp_name,
            "ocpp_code": self.ocpp_code
        }

    def to_json(self):
        return json.dumps(self.dict, ensure_ascii=False)


class Pod:
    def __init__(self, data: Dict[str, Any]):
        helpers = Helpers()

        self.id: int                   = data.get('id', None)
        self.name: str                 = data.get('name', None)
        self.ppid: str                 = data.get('ppid', None)
        self.payg: bool                = data.get('payg', None)
        self.home: bool                = data.get('home', None)
        self.public: bool              = data.get('public', None)
        self.ev_zone: bool              = data.get('evZone', None)
        self.address_id: int           = data.get('address_id', None)
        self.description: str          = data.get('description', "")
        self.commissioned_at: datetime = helpers.lazy_convert_to_datetime(data.get('commissioned_at', None))
        self.created_at: datetime      = helpers.lazy_convert_to_datetime(data.get('created_at', None))
        self.last_contact_at: datetime = helpers.lazy_convert_to_datetime(data.get('last_contact_at', None))
        self.contactless_enabled: bool = data.get('contactless_enabled', None)
        self.unit_id: int              = data.get('unit_id', None)
        self.timezone: str             = data.get('timezone', None)
        self.price: int                = data.get('price', None)

        model_data = data.get('model', {})
        self.model = self.Model(
            id                   = model_data.get('id', None),
            name                 = model_data.get('name', None),
            vendor               = model_data.get('vendor', None),
            supports_payg        = model_data.get('supports_payg', False),
            supports_ocpp        = model_data.get('supports_ocpp', False),
            supports_contactless = model_data.get('supports_contactless', False),
            image_url            = model_data.get('image_url', None)
        )

        location_data = data.get('location', {})
        self.location = self.Location(
            lat = location_data.get('lat', 0.0),
            lng = location_data.get('lng', 0.0)
        )

        self.statuses = []
        statuses_data = data.get('statuses', [])
        for status in statuses_data:
            self.statuses.append(
                self.Status(
                    id       = status.get('id', None),
                    name     = status.get('name', None),
                    key_name = status.get('key_name', None),
                    label    = status.get('label', None),
                    door     = status.get('door', None),
                    door_id  = status.get('door_id', None),
                )
            )

        self.unit_connectors = []
        unit_connectors_data = data.get('unit_connectors', [])
        for unit_connector in unit_connectors_data:
            connector_data = unit_connector.get('connector', {})

            socket_obj = None
            socket_data = connector_data.get('socket', None)
            if socket_data is not None:
                socket_obj = Socket(
                    type = socket_data.get('type', None),
                    description = socket_data.get('description', None),
                    ocpp_name = socket_data.get('ocpp_name', None),
                    ocpp_code = socket_data.get('ocpp_code', None),
                )

            self.unit_connectors.append(
                self.Connector(
                    id = connector_data.get('id', None),
                    door = connector_data.get('door', None),
                    door_id = connector_data.get('door_id', None),
                    power = connector_data.get('power', None),
                    current = connector_data.get('current', None),
                    voltage = connector_data.get('voltage', None),
                    charge_method = connector_data.get('charge_method', None),
                    has_cable = connector_data.get('has_cable', None),
                    socket=socket_obj
                )
            )

        self.charge_schedules = []
        charge_schedules_data = data.get('charge_schedules', [])
        for charge_schedule_data in charge_schedules_data:
            status_data = charge_schedule_data.get('status', None)
            status_obj = None
            if status_data:
                status_obj = ScheduleStatus(
                    is_active = status_data.get('is_active', None)
                )

            self.charge_schedules.append(
                Schedule(
                    uid = charge_schedule_data.get('uid', None),
                    start_day = charge_schedule_data.get('start_day', None),
                    start_time = charge_schedule_data.get('start_time', None),
                    end_day = charge_schedule_data.get('end_day', None),
                    end_time = charge_schedule_data.get('end_time', None),
                    status = status_obj
                )
            )
    
    @property
    def dict(self) -> Dict[str, Any]:
        helpers = Helpers()
        
        d = {
            "id": self.id,
            "name": self.name,
            "ppid": self.ppid,
            "payg": self.payg,
            "home": self.home,
            "public": self.public,
            "evZone": self.ev_zone,
            "location": self.location.dict,
            "address_id": self.address_id,
            "description": self.description,
            "commissioned_at": helpers.lazy_iso_format_datetime(self.commissioned_at),
            "created_at": helpers.lazy_iso_format_datetime(self.created_at),
            "last_contact_at": helpers.lazy_iso_format_datetime(self.last_contact_at),
            "contactless_enabled": self.contactless_enabled,
            "unit_id": self.unit_id,
            "timezone": self.timezone,
            "model": self.model.dict,
            "price": self.price,
            "statuses": [],
            "unit_connectors": [],
            "charge_schedules": []
        }

        for status in self.statuses:
            d['statuses'].append(status.dict)

        for unit_connector in self.unit_connectors:
            d['unit_connectors'].append(
                { "connector": unit_connector.dict }
            )

        for charge_schedule in self.charge_schedules:
            d['charge_schedules'].append(charge_schedule.dict)

        return d
    
    def to_json(self):
        return json.dumps(self.dict, ensure_ascii=False)


    @dataclass
    class Model:
        id: int
        name: str
        vendor: str
        supports_payg: bool = False
        supports_ocpp: bool = False
        supports_contactless: bool = False
        image_url: str = None

        @property
        def model(self):
            return self.name

        @property
        def dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "vendor": self.vendor,
                "supports_payg": self.supports_payg,
                "supports_ocpp": self.supports_ocpp,
                "supports_contactless": self.supports_contactless,
                "image_url": self.image_url
            }

        def to_json(self):
            return json.dumps(self.dict, ensure_ascii=False)


    @dataclass
    class Location:
        lat: float
        lng: float

        @property
        def dict(self):
            return {
                "lat": self.lat,
                "lng": self.lng
            }

        def to_json(self):
            return json.dumps(self.dict, ensure_ascii=False)

    
    @dataclass
    class Status:
        id: int
        name: StatusName
        key_name: StatusKeyName
        label: StatusName
        door: str
        door_id: int

        @property
        def dict(self):
            return {
                "id": self.id,
                "name": self.name,
                "key_name": self.key_name,
                "label": self.label,
                "door": self.door,
                "door_id": self.door_id
            }

        def to_json(self):
            return json.dumps(self.dict, ensure_ascii=False)

    
    @dataclass
    class Connector:
        id: int
        door: str
        door_id: int
        power: int
        current: int
        voltage: int
        charge_method: str
        has_cable: bool
        socket: Socket

        @property
        def dict(self):
            return {
                "id": self.id,
                "door": self.door,
                "door_id": self.door_id,
                "power": self.power,
                "current": self.current,
                "voltage": self.voltage,
                "charge_method": self.charge_method,
                "has_cable": self.has_cable,
                "socket": self.socket.dict
            }

        def to_json(self):
            return json.dumps(self.dict, ensure_ascii=False)
