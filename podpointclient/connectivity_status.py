"""Connectivity State class, represents a 'Connectivity State' from the podpoint apis"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass, field
from .helpers.functions import lazy_convert_to_datetime, lazy_iso_format_datetime
import json

# {
# 	"ppid": "PSL-266056",
# 	"evses": [{
# 		"id": 1,
# 		"connectivityState": {
# 			"protocol": "POW",
# 			"connectivityStatus": "ONLINE",
# 			"signalStrength": -68,
# 			"lastMessageAt": "2024-04-05T18:36:29Z",
# 			"connectionStartedAt": "2024-04-05T18:26:26.819Z",
# 			"connectionQuality": 3
# 		},
# 		"connectors": [{
# 			"id": 1,
# 			"door": "A",
# 			"chargingState": "SUSPENDED_EV"
# 		}],
# 		"architecture": "arch3",
# 		"energyOfferStatus": {
# 			"isOfferingEnergy": true,
# 			"reason": "CHARGE_SCHEDULE",
# 			"until": null,
# 			"randomDelay": null,
# 			"doNotCache": false
# 		}
# 	}],
# 	"connectedComponents": ["evses"]
# }

@dataclass
class Evse:
    """Represents a Location within a charge from pod point"""

    def __init__(self, data: Dict[str, Any]):
        self.id: int = data.get('id', None)
        self.architecture: str = data.get('architecture', None)

        connectivity_state_data = data.get('connectivityState', {})
        self.connectivity_state = self.ConnectivityState(data=connectivity_state_data)

        connectors_data = data.get('connectors', [])
        self.connectors = []
        for connector in connectors_data:
            self.connectors.append(self.Connector(data=connector))

        energy_offer_status_data = data.get('energyOfferStatus', {})
        self.energy_offer_status = self.EnergyOfferStatus(data=energy_offer_status_data)

    @property
    def dict(self):
        return {
            "id": self.id,
            "architecture": self.architecture,
            "connectivityState": self.connectivity_state.dict,
            "connectors": [connector.dict for connector in self.connectors],
            "energyOfferStatus": self.energy_offer_status.dict
        }

    def to_json(self):
        """JSON representation of a ConnectivityState object"""
        return json.dumps(self.dict, ensure_ascii=False)

    @dataclass
    class ConnectivityState:
        """Represents a Location within a charge from pod point"""

        def __init__(self, data: Dict[str, Any]):
            self.protocol: str = data.get('protocol', None)
            self.connectivity_status: str = data.get('connectivityStatus', None)
            self.signal_strength:int = data.get('signalStrength', None)
            self.last_message_at: datetime = lazy_convert_to_datetime(data.get('lastMessageAt', None))
            self.connection_started_at: datetime = lazy_convert_to_datetime(data.get('connectionStartedAt', None))
            self.connection_quality: int = data.get('connectionQuality', None)

        @property
        def dict(self):
            return {
                "protocol": self.protocol,
                "connectivityStatus": self.connectivity_status,
                "signalStrength": self.signal_strength,
                "lastMessageAt": lazy_iso_format_datetime(self.last_message_at),
                "connectionStartedAt": lazy_iso_format_datetime(self.connection_started_at),
                "connectionQuality": self.connection_quality
            }

        def to_json(self):
            """JSON representation of a ConnectivityState object"""
            return json.dumps(self.dict, ensure_ascii=False)

    @dataclass
    class Connector:
        """Represents a Location within a charge from pod point"""

        def __init__(self, data: Dict[str, Any]):
            self.id: int = data.get('id', None)
            self.door: str = data.get('door', None)
            self.charging_state: str = data.get('chargingState', None)

        @property
        def dict(self):
            return {
                "id": self.id,
                "door": self.door,
                "chargingState": self.charging_state
            }

    def to_json(self):
        """JSON representation of a ConnectivityState object"""
        return json.dumps(self.dict, ensure_ascii=False)

    @dataclass
    class EnergyOfferStatus:
        """Represents a Location within a charge from pod point"""

        def __init__(self, data: Dict[str, Any]):
            self.is_offering_energy: bool = data.get('isOfferingEnergy', None)
            self.reason: str = data.get('reason', None)
            self.until: datetime = lazy_convert_to_datetime(data.get('until', None))
            self.random_delay = data.get('randomDelay', None)
            self.do_not_cache: bool = data.get('doNotCache', None)

        @property
        def dict(self):
            return {
                "isOfferingEnergy": self.is_offering_energy,
                "reason": self.reason,
                "until": lazy_iso_format_datetime(self.until),
                "randomDelay": self.random_delay,
                "doNotCache": self.do_not_cache
            }

        def to_json(self):
            """JSON representation of a ConnectivityState object"""
            return json.dumps(self.dict, ensure_ascii=False)


class ConnectivityStatus:
    """Representation of a Connectivity State from pod point"""

    def __init__(self, data: Dict[str, Any]):
        self.ppid: int = data.get('ppid', None)
        self.connected_components: List[str] = data.get('connectedComponents', [])

        self.evses: List[Evse] = []
        for evse in data.get('evses', []):
            self.evses.append(Evse(data=evse))

    @property
    def dict(self) -> Dict[str, Any]:
        return {
            "ppid": self.ppid,
            "connected_components": self.connected_components,
            "evses": [evse.dict for evse in self.evses]
        }

    @property
    def connectivity_status(self):
        """Return the connectivity status of the first evse"""
        evse = self.evses[0]
        if evse is None:
            return None

        connectivity_state = evse.connectivity_state
        if connectivity_state is None:
            return None

        return connectivity_state.connectivity_status

    @property
    def connectivity_status(self):
        """Return the connectivity status of the first evse"""
        evse = self.evses[0]
        if evse is None:
            return None

        connectivity_state = evse.connectivity_state
        if connectivity_state is None:
            return None

        return connectivity_state.connectivity_status

    @property
    def last_message_at(self):
        """Return the last message at of the first evse"""
        evse = self.evses[0]
        if evse is None:
            return None

        connectivity_state = evse.connectivity_state
        if connectivity_state is None:
            return None

        return connectivity_state.last_message_at

    @property
    def charging_state(self):
        """Return the charging state of the first evse"""
        evse = self.evses[0]
        if evse is None:
            return None

        connector = evse.connectors[0]
        if connector is None:
            return None

        return connector.charging_state

    @property
    def offering_energy(self):
        """Return the offering energy of the first evse"""
        evse = self.evses[0]
        if evse is None:
            return None

        energy_offer_status = evse.energy_offer_status
        if energy_offer_status is None:
            return None

        return energy_offer_status.is_offering_energy

    def to_json(self):
        """JSON representation of a ConnectivityState object"""
        return json.dumps(self.dict, ensure_ascii=False)
