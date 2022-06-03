"""Representation of a Schedule from pod point"""
from dataclasses import dataclass
import json

@dataclass
class ScheduleStatus:
    """Representation of a Status within a Schedule from pod point"""
    is_active: bool = False

@dataclass
class Schedule:
    """Representation of a Schedule from pod point"""
    start_day: int
    start_time: str
    end_day: int
    end_time: str
    status: ScheduleStatus
    uid: str = None # Optional uid value - new schedules dont require uid and is easier to ommit

    @property
    def is_active(self):
        """Is this schedule active?"""
        return self.status.is_active

    @property
    def dict(self):
        """Dictionary representation of a Schedule"""
        dictionary = {
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
            uid_dictionary = {"uid": self.uid}
            uid_dictionary.update(dictionary)
            dictionary = uid_dictionary

        return dictionary

    def to_json(self):
        """JSON representation of a Schedule"""
        return json.dumps(self.dict, ensure_ascii=False)
