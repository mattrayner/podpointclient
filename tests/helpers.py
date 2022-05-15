import json
import os

from isort import code
from podpointclient.endpoints import API_BASE_URL, AUTH, CHARGE_SCHEDULES, PODS, SESSIONS, UNITS, USERS

class Mocks:
    def __init__(self, m = None) -> None:
        self.m = m

    def happy_path(self):
        auth_response = self.auth_response()
        session_response = self.session_response()
        pods_response = self.pods_response()
        pods_response_schedule_disabled = self.pods_response_schedule_disabled()

        self.m.post(f'{API_BASE_URL}{AUTH}', payload=auth_response)
        self.m.post(f'{API_BASE_URL}{SESSIONS}', payload=session_response)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=all&include=statuses,price,model,unit_connectors,charge_schedules&timestamp=1640995200.0', payload=pods_response)
        self.m.put(f'{API_BASE_URL}{UNITS}/198765{CHARGE_SCHEDULES}?timestamp=1640995200.0', payload=pods_response, status=201)
        self.m.get(f'{API_BASE_URL}{USERS}/1234{PODS}?perpage=all&include=statuses,price,model,unit_connectors,charge_schedules&timestamp=1640995200.0', payload=pods_response_schedule_disabled)

    def auth_response(self):
        return self.__json_load_fixture('auth')

    def session_response(self):
        return self.__json_load_fixture('session')

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

    def __json_load_fixture(self, fixture_name: str):
        file_location = os.path.dirname(__file__)
        path = f'fixtures/{fixture_name}.json'
        abs_file_path = os.path.join(file_location, path)
        return json.load(open(abs_file_path))