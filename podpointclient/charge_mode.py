from strenum import StrEnum

class ChargeMode(StrEnum):
    """An ENUM representing the current charge mode"""
    MANUAL   = "Manual"
    SMART    = "Smart"
    OVERRIDE = "Override"