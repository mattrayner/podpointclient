import json
import os

from podpointclient.endpoints import GOOGLE_BASE_URL, PASSWORD_VERIFY, API_BASE_URL, AUTH, CHARGE_SCHEDULES, PODS, SESSIONS, UNITS, USERS, CHARGES, FIRMWARE, GOOGLE_TOKEN_BASE_URL, TOKEN

class Mocks:
    def __init__(self, m = None) -> None:
        self.m = m

    def happy_path(self, include_timestamp=False):
        auth_response = self.auth_response()
        refresh_response = self.refresh_response()
        session_response = self.session_response()
        pods_response = self.pods_response()
        pods_response_schedule_disabled = self.pods_response_schedule_disabled()
        charges_response = self.charges_response()
        firmware_response = self.firmware_response()
        user_response = self.user_response()

        timestamp = ""
        and_timestamp = ""
        question_timestamp = ""
        if include_timestamp:
            timestamp = 'timestamp=1640995200.0'
            and_timestamp = f'&{timestamp}'
            question_timestamp = f'?{timestamp}'

        self.m.post(f'{GOOGLE_BASE_URL}{PASSWORD_VERIFY}', payload=auth_response)
        self.m.post(f'{GOOGLE_TOKEN_BASE_URL}{TOKEN}', payload=refresh_response)
        self.m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=1&page=1{and_timestamp}', payload=pods_response)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=5&page=1&include=statuses,price,model,unit_connectors,charge_schedules,charge_override{and_timestamp}', payload=pods_response)
        self.m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}{question_timestamp}', payload=pods_response, status=201)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=5&page=1&include=statuses,price,model,unit_connectors,charge_schedules,charge_override{and_timestamp}', payload=pods_response_schedule_disabled)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=1&page=1{and_timestamp}', payload=charges_response)
        self.m.get(f'{API_BASE_URL}{UNITS}/198765{FIRMWARE}{question_timestamp}', payload=firmware_response)
        self.m.get(f'{API_BASE_URL}{AUTH}?include=account,vehicle,vehicle.make,unit.pod.unit_connectors,unit.pod.statuses,unit.pod.model,unit.pod.charge_schedules,unit.pod.charge_override', payload=user_response)

    def auth_response(self):
        return self.__json_load_fixture('auth')

    def refresh_response(self):
        return self.__json_load_fixture('refresh')

    def session_response(self):
        return self.__json_load_fixture('session')

    def charge_response(self):
        return self.__json_load_fixture('complete_charges')

    def pods_response(self, pod_count: int = 1):
        pod = self.complete_pod()

        pods = []
        for i in range(pod_count):
            pods.append(pod)

        return { "pods": pods }

    def pods_response_schedule_disabled(self, pod_count: int = 1):
        pod = self.complete_pod_schedule_disabled()

        pods = []
        for i in range(pod_count):
            pods.append(pod)

        return { "pods": pods }

    def complete_pod(self):
        return self.__json_load_fixture('complete_pod')

    def complete_pod_schedule_disabled(self):
        return self.__json_load_fixture('complete_pod_disabled_schedule')
    
    def charges_response(self):
        return self.__json_load_fixture('complete_charges')

    def firmware_response(self):
        return self.__json_load_fixture('complete_firmware')

    def user_response(self):
        return self.__json_load_fixture('complete_user')

    def __json_load_fixture(self, fixture_name: str):
        file_location = os.path.dirname(__file__)
        path = f'fixtures/{fixture_name}.json'
        abs_file_path = os.path.join(file_location, path)
        return json.load(open(abs_file_path))