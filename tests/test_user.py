import imp

from aioresponses import aioresponses
import aiohttp
from podpointclient.user import User, Address, Image, Vehicle, VehicleMake, Unit
from typing import List
from podpointclient.pod import Pod
import pytest
from freezegun import freeze_time
import json
from helpers import Mocks

from podpointclient.endpoints import API_BASE_URL, AUTH

def test_empty_user():
    user = User(data={})
    assert None is user.id
    assert None is user.email
    assert None is user.first_name
    assert None is user.last_name
    assert None is user.role
    assert 0 == user.hasHomeCharge
    assert None is user.locale
    assert user.preferences == []
    assert None is user.account
    assert None is user.vehicle
    assert None is user.unit

    assert user.dict == {
        'email': None,
        'first_name': None,
        'hasHomeCharge': 0,
        'id': None,
        'last_name': None,
        'locale': None,
        'preferences': [],
        'role': None
    }
    assert user.to_json() == '{"id": null, "email": null, "first_name": null, "last_name": null, "role": null, "hasHomeCharge": 0, "locale": null, "preferences": []}'

def test_complete_user():
    user_data = Mocks().user_response()['users']
    user = User(data=user_data)
    assert 123456 == user.id
    assert "podpoint@example.com" == user.email
    assert "Example" == user.first_name
    assert "User" == user.last_name
    assert "user" == user.role
    assert 1 == user.hasHomeCharge
    assert "en" == user.locale

    assert 1 == len(user.preferences)
    assert isinstance(user.preferences[0], User.UserPreference) is True

    assert isinstance(user.account, User.UserAccount) is True
    assert 123456 == user.account.user_id
    assert "1a756c9b-dfac-4c2a-ba13-9cdcc2399366" == user.account.uid
    assert 173 == user.account.balance
    assert "GBP" == user.account.currency

    assert isinstance(user.account.billing_address, Address) is True
    assert "" == user.account.billing_address.business_name
    assert "" == user.account.billing_address.address1
    assert "" == user.account.billing_address.address2
    assert "" == user.account.billing_address.town
    assert "" == user.account.billing_address.postcode
    assert "" == user.account.billing_address.country

    assert "" == user.account.phone
    assert user.account.mobile is None
    
    assert isinstance(user.vehicle, Vehicle) is True
    assert 129 == user.vehicle.id
    assert "citroenC5AircrossPlugInHybrid" == user.vehicle.uuid
    assert "C5 Aircross Plug-in Hybrid" == user.vehicle.name
    assert 7 == user.vehicle.capacity
    assert 13.2 == user.vehicle.batteryCapacity
    assert None is user.vehicle.startYear
    assert None is user.vehicle.endYear

    assert isinstance(user.vehicle.image, Image) is True
    assert "https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png?w=0.5&h=0.5" == user.vehicle.image.half_size
    assert "https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png?w=0.75&h=0.75" == user.vehicle.image.seventy_five_percent
    assert "https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png" == user.vehicle.image.original

    assert isinstance(user.vehicle.make, VehicleMake) is True
    assert 22 == user.vehicle.make.id
    assert "Citroen" == user.vehicle.make.name

    assert isinstance(user.vehicle.make.logo, Image) is True
    assert "https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png?w=0.5&h=0.5" == user.vehicle.make.logo.half_size
    assert "https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png?w=0.75&h=0.75" == user.vehicle.make.logo.seventy_five_percent
    assert "https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png" == user.vehicle.make.logo.original

    assert isinstance(user.unit, Unit) is True
    assert 123456 == user.unit.id
    assert "211092" == user.unit.ppid
    assert None is user.unit.name
    assert "Available" == user.unit.status
    assert "soloArch3" == user.unit.architecture

    assert isinstance(user.unit.pod, Pod) is True

    assert user.dict == {'account': {'balance': 173,
                      'billing_address': {'address1': '',
                                          'address2': '',
                                          'business_name': '',
                                          'country': '',
                                          'postcode': '',
                                          'town': ''},
                      'currency': 'GBP',
                      'mobile': None,
                      'phone': '',
                      'uid': '1a756c9b-dfac-4c2a-ba13-9cdcc2399366',
                      'user_id': 123456},
          'email': 'podpoint@example.com',
          'first_name': 'Example',
          'hasHomeCharge': 1,
          'id': 123456,
          'last_name': 'User',
          'locale': 'en',
          'preferences': [{'unitOfDistance': 'mi'}],
          'role': 'user',
          'unit': {'architecture': 'soloArch3',
                   'id': 123456,
                   'name': None,
                   'pod': {'address_id': 12345,
                           'charge_schedules': [{'end_day': 1,
                                                 'end_time': '00:00:01',
                                                 'start_day': 1,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': '2e47721e-cdb2-49d7-ba47-f956975b7ed5'},
                                                {'end_day': 2,
                                                 'end_time': '00:00:01',
                                                 'start_day': 2,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': 'bf3188eb-745e-4fbd-baa9-8a141eb708ed'},
                                                {'end_day': 3,
                                                 'end_time': '00:00:01',
                                                 'start_day': 3,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': '80eeba4b-2e69-4e04-a1e9-6e7dfc88528e'},
                                                {'end_day': 4,
                                                 'end_time': '00:00:01',
                                                 'start_day': 4,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': '3fddde7d-0809-43b3-8d16-64faf8a84e97'},
                                                {'end_day': 5,
                                                 'end_time': '00:00:01',
                                                 'start_day': 5,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': '79e69a06-2c3a-442b-a65f-5766140d8874'},
                                                {'end_day': 6,
                                                 'end_time': '00:00:01',
                                                 'start_day': 6,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': '0d2e6fdc-2a3d-4808-84e1-22e1d9d10be8'},
                                                {'end_day': 7,
                                                 'end_time': '00:00:01',
                                                 'start_day': 7,
                                                 'start_time': '00:00:00',
                                                 'status': {'is_active': False},
                                                 'uid': 'f79028be-00e9-4a86-a6c4-d474b7aaab37'}],
                           'commissioned_at': '2022-01-25T09:00:00+00:00',
                           'contactless_enabled': False,
                           'created_at': '2022-02-13T10:39:05+00:00',
                           'current_kwh': 0.0,
                           'description': '',
                           'evZone': False,
                           'firmware': None,
                           'home': True,
                           'id': 123456,
                           'last_contact_at': '2023-01-10T19:17:12+00:00',
                           'location': {'lat': 23.543643, 'lng': 7.2434543},
                           'model': {'id': 256,
                                     'image_url': None,
                                     'name': 'S7-UC-03-ACA',
                                     'supports_contactless': False,
                                     'supports_ocpp': False,
                                     'supports_payg': False,
                                     'vendor': 'Pod Point'},
                           'name': None,
                           'payg': False,
                           'ppid': 'PSL-211092',
                           'price': None,
                           'public': False,
                           'statuses': [{'door': 'A',
                                         'door_id': 1,
                                         'id': 1,
                                         'key_name': 'available',
                                         'label': 'Available',
                                         'name': 'Available'}],
                           'timezone': 'UTC',
                           'total_charge_seconds': 0,
                           'total_cost': 0,
                           'total_kwh': 0.0,
                           'unit_connectors': [{'connector': {'charge_method': 'Single '
                                                                               'Phase '
                                                                               'AC',
                                                              'current': 32,
                                                              'door': 'A',
                                                              'door_id': 1,
                                                              'has_cable': False,
                                                              'id': 303,
                                                              'power': 7,
                                                              'socket': {'description': 'Type '
                                                                                        '2 '
                                                                                        'socket',
                                                                         'ocpp_code': 3,
                                                                         'ocpp_name': 'sType2',
                                                                         'type': 'IEC '
                                                                                 '62196-2 '
                                                                                 'Type '
                                                                                 '2'},
                                                              'voltage': 230}}],
                           'unit_id': 123456},
                   'ppid': '211092',
                   'status': 'Available'},
          'vehicle': {'batteryCapacity': 13.2,
                      'capacity': 7,
                      'endYear': None,
                      'id': 129,
                      'image': {'@1x': 'https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png?w=0.5&h=0.5',
                                '@2x': 'https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png?w=0.75&h=0.75',
                                '@3x': 'https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png'},
                      'make': {'id': 22,
                               'logo': {'@1x': 'https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png?w=0.5&h=0.5',
                                        '@2x': 'https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png?w=0.75&h=0.75',
                                        '@3x': 'https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png'},
                               'name': 'Citroen'},
                      'name': 'C5 Aircross Plug-in Hybrid',
                      'startYear': None,
                      'uuid': 'citroenC5AircrossPlugInHybrid'}}
    assert user.to_json() == '{"id": 123456, "email": "podpoint@example.com", "first_name": "Example", "last_name": "User", "role": "user", "hasHomeCharge": 1, "locale": "en", "preferences": [{"unitOfDistance": "mi"}], "account": {"user_id": 123456, "uid": "1a756c9b-dfac-4c2a-ba13-9cdcc2399366", "balance": 173, "currency": "GBP", "billing_address": {"business_name": "", "address1": "", "address2": "", "town": "", "postcode": "", "country": ""}, "phone": "", "mobile": null}, "vehicle": {"id": 129, "uuid": "citroenC5AircrossPlugInHybrid", "name": "C5 Aircross Plug-in Hybrid", "capacity": 7, "batteryCapacity": 13.2, "startYear": null, "endYear": null, "image": {"@1x": "https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png?w=0.5&h=0.5", "@2x": "https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png?w=0.75&h=0.75", "@3x": "https://pod-point-admin-images-prod.imgix.net/vehicle-model-images/8eb13aeaf566eaedbe648bab8a5c14c0.png"}, "make": {"id": 22, "name": "Citroen", "logo": {"@1x": "https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png?w=0.5&h=0.5", "@2x": "https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png?w=0.75&h=0.75", "@3x": "https://pod-point-admin-images-prod.imgix.net/vehicle-make-logos/315261a80a1287b6d1b70f5c0fa8ccde.png"}}}, "unit": {"id": 123456, "ppid": "211092", "name": null, "status": "Available", "architecture": "soloArch3", "pod": {"id": 123456, "name": null, "ppid": "PSL-211092", "payg": false, "home": true, "public": false, "evZone": false, "location": {"lat": 23.543643, "lng": 7.2434543}, "address_id": 12345, "description": "", "commissioned_at": "2022-01-25T09:00:00+00:00", "created_at": "2022-02-13T10:39:05+00:00", "last_contact_at": "2023-01-10T19:17:12+00:00", "contactless_enabled": false, "unit_id": 123456, "timezone": "UTC", "model": {"id": 256, "name": "S7-UC-03-ACA", "vendor": "Pod Point", "supports_payg": false, "supports_ocpp": false, "supports_contactless": false, "image_url": null}, "price": null, "statuses": [{"id": 1, "name": "Available", "key_name": "available", "label": "Available", "door": "A", "door_id": 1}], "unit_connectors": [{"connector": {"id": 303, "door": "A", "door_id": 1, "power": 7, "current": 32, "voltage": 230, "charge_method": "Single Phase AC", "has_cable": false, "socket": {"type": "IEC 62196-2 Type 2", "description": "Type 2 socket", "ocpp_name": "sType2", "ocpp_code": 3}}}], "charge_schedules": [{"uid": "2e47721e-cdb2-49d7-ba47-f956975b7ed5", "start_day": 1, "start_time": "00:00:00", "end_day": 1, "end_time": "00:00:01", "status": {"is_active": false}}, {"uid": "bf3188eb-745e-4fbd-baa9-8a141eb708ed", "start_day": 2, "start_time": "00:00:00", "end_day": 2, "end_time": "00:00:01", "status": {"is_active": false}}, {"uid": "80eeba4b-2e69-4e04-a1e9-6e7dfc88528e", "start_day": 3, "start_time": "00:00:00", "end_day": 3, "end_time": "00:00:01", "status": {"is_active": false}}, {"uid": "3fddde7d-0809-43b3-8d16-64faf8a84e97", "start_day": 4, "start_time": "00:00:00", "end_day": 4, "end_time": "00:00:01", "status": {"is_active": false}}, {"uid": "79e69a06-2c3a-442b-a65f-5766140d8874", "start_day": 5, "start_time": "00:00:00", "end_day": 5, "end_time": "00:00:01", "status": {"is_active": false}}, {"uid": "0d2e6fdc-2a3d-4808-84e1-22e1d9d10be8", "start_day": 6, "start_time": "00:00:00", "end_day": 6, "end_time": "00:00:01", "status": {"is_active": false}}, {"uid": "f79028be-00e9-4a86-a6c4-d474b7aaab37", "start_day": 7, "start_time": "00:00:00", "end_day": 7, "end_time": "00:00:01", "status": {"is_active": false}}], "total_kwh": 0.0, "total_charge_seconds": 0, "current_kwh": 0.0, "total_cost": 0, "firmware": null}}}'
