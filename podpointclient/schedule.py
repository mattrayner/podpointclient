from dataclasses import dataclass
import json
from typing import Any, Optional

@dataclass
class ScheduleStatus:
    is_active: bool = False

@dataclass
class Schedule:
    start_day: int
    start_time: str
    end_day: int
    end_time: str
    status: ScheduleStatus
    uid: str = None # Optional uid value - when creating new schedules uid is not required and is easier to ommit

    @property
    def is_active(self):
        return self.status.is_active

    @property
    def dict(self):
        d = {
            "start_day": self.start_day,
            "start_time": self.start_time,
            "end_day": self.end_day,
            "end_time": self.end_time,
            "status": {
                "is_active": self.status.is_active
            }
        }

        # If uid is set, add it to the start
        if self.uid:
          ud = {"uid": self.uid}
          ud.update(d)
          d = ud

        return d

    def to_json(self):
        return json.dumps(self.dict, ensure_ascii=False)
