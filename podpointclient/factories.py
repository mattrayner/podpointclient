import sched
from typing import Dict, Any, List
from podpointclient.pod import Pod
from podpointclient.schedule import Schedule, ScheduleStatus

class PodFactory:
    def build_pods(self, pods_reponse: Dict[str, Any]) -> List[Pod]:
        pods = []

        pods_data = pods_reponse.get('pods', None) 
        if pods_data is None:
            return pods

        for pod_data in pods_data:
            pods.append(Pod(data=pod_data))

        return pods

class ScheduleFactory:
    def build_schedules(self, enabled: bool, start_time: str = "00:00:00", end_time: str = "00:00:01") -> List[Schedule]:
        schedules = []

        for i in range(7):
            day = i + 1

            schedule = Schedule(
                start_day=i,
                start_time=start_time,
                end_day=i,
                end_time=end_time,
                status=ScheduleStatus(is_active=enabled)
            )

            schedules.append(schedule)

        return schedules