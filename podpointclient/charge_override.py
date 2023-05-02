"""Charge Override class, represents a 'Charge Override' from the podpoint apis"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass, field
from .helpers.functions import lazy_convert_to_datetime, lazy_iso_format_datetime

class ChargeOverride:
    """Representation of a Charge Override from pod point"""
    def __init__(self, data: Dict[str, Any]):
        self.ppid: int              = data.get('ppid', None)
        self.requested_at: datetime = lazy_convert_to_datetime(data.get('requested_at', None))
        self.received_at: datetime  = lazy_convert_to_datetime(data.get('received_at', None))
        self.ends_at: datetime      = lazy_convert_to_datetime(data.get('ends_at', None))


    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "ppid": self.ppid,
            "requested_at": lazy_iso_format_datetime(self.requested_at),
            "received_at": lazy_iso_format_datetime(self.received_at),
            "ends_at": lazy_iso_format_datetime(self.ends_at)
        }

    def to_json(self):
        """JSON representation of a ChargeOverride object"""
        return json.dumps(self.dict, ensure_ascii=False)

    @property
    def active(self) -> bool:
        """Is the charge override active"""
        return (self.ends_at is not None and self.ends_at > datetime.now(self.ends_at.tzinfo))

    @property
    def remaining_time(self) -> timedelta:
        """How long is left for the charge override"""
        if self.active is False:
            return None

        return self.ends_at - datetime.now(self.ends_at.tzinfo)
