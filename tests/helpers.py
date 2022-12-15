import json
import os

from podpointclient.endpoints import API_BASE_URL, AUTH, CHARGE_SCHEDULES, PODS, SESSIONS, UNITS, USERS, CHARGES

class Mocks:
    def __init__(self, m = None) -> None:
        self.m = m

    def happy_path(self, include_timestamp=False):
        auth_response = self.auth_response()
        session_response = self.session_response()
        pods_response = self.pods_response()
        pods_response_schedule_disabled = self.pods_response_schedule_disabled()
        charges_response = self.charges_response()

        timestamp = ""
        and_timestamp = ""
        question_timestamp = ""
        if include_timestamp:
            timestamp = 'timestamp=1640995200.0'
            and_timestamp = f'&{timestamp}'
            question_timestamp = f'?{timestamp}'

        self.m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        self.m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=1&page=1{and_timestamp}', payload=pods_response)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=5&page=1&include=statuses,price,model,unit_connectors,charge_schedules{and_timestamp}', payload=pods_response)
        self.m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}{question_timestamp}', payload=pods_response, status=201)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=5&page=1&include=statuses,price,model,unit_connectors,charge_schedules{and_timestamp}', payload=pods_response_schedule_disabled)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{CHARGES}?perpage=1&page=1{and_timestamp}', payload=charges_response)

    def auth_response(self):
        return self.__json_load_fixture('auth')

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

    def __json_load_fixture(self, fixture_name: str):
        file_location = os.path.dirname(__file__)
        path = f'fixtures/{fixture_name}.json'
        abs_file_path = os.path.join(file_location, path)
        return json.load(open(abs_file_path))