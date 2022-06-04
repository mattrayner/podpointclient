"""Factories used to create top level objects such as pods, sessions and charges"""
from typing import Dict, Any, List
from .pod import Pod
from .schedule import Schedule, ScheduleStatus
from .charge import Charge

class PodFactory:
    """Factory for creating Pod objects"""
    def build_pods(self, pods_response: Dict[str, Any]) -> List[Pod]:
        """Build a number of pod objects based off of a response from pod point"""
        pods = []

        pods_data = pods_response.get('pods', None)
        if pods_data is None:
            return pods

        for pod_data in pods_data:
            pods.append(Pod(data=pod_data))

        return pods

class ScheduleFactory:
    """Factory for creating Schedule objects"""
    def build_schedules(
        self,
        enabled: bool,
        start_time: str = "00:00:00",
        end_time: str = "00:00:01"
    ) -> List[Schedule]:
        """Build a number of schedule objects based off of a response from pod point"""
        schedules = []

        for iterator in range(7):
            day = iterator + 1

            schedule = Schedule(
                start_day=day,
                start_time=start_time,
                end_day=day,
                end_time=end_time,
                status=ScheduleStatus(is_active=enabled)
            )

            schedules.append(schedule)

        return schedules


class ChargeFactory:
    """Factory  for creating Charge objects"""
    def build_charges(self, charge_response: Dict[str, Any]) -> List[Charge]:
        """Build a list of charge objects based off of a response from pod point"""
        charges = []

        charge_data = charge_response.get('charges', None)
        if charge_data is None:
            return charges

        for charge in charge_data:
            charges.append(Charge(data=charge))

        return charges
