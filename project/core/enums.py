"""
Core enums for network monitoring.

This module defines enumeration types used throughout the application
for representing network connection quality, network types, and measurement status.
"""

from enum import Enum, auto


class ConnectionQuality(Enum):
    """
    Network connection quality rating.

    Based on latency, jitter, packet loss, and speed measurements.
    """

    EXCELLENT = auto()
    GOOD = auto()
    FAIR = auto()
    POOR = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return self.name.capitalize()


class NetworkType(Enum):
    """
    Type of network connection.

    Used to identify the physical/logical connection type.
    """

    WIFI = auto()
    ETHERNET = auto()
    MOBILE = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return self.name.capitalize()


class SignalStrength(Enum):
    """
    WiFi signal strength rating.

    Based on RSSI (Received Signal Strength Indicator) in dBm.
    - EXCELLENT: -50 dBm or better
    - GOOD: -60 dBm or better
    - FAIR: -70 dBm or better
    - POOR: -80 dBm or better
    - VERY_POOR: worse than -80 dBm
    """

    EXCELLENT = auto()
    GOOD = auto()
    FAIR = auto()
    POOR = auto()
    VERY_POOR = auto()
    UNKNOWN = auto()

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return self.name.replace("_", " ").capitalize()


class MeasurementStatus(Enum):
    """
    Status of network measurement operation.

    Indicates the current state or result of a measurement attempt.
    """

    IDLE = auto()
    IN_PROGRESS = auto()
    SUCCESS = auto()
    FAILED = auto()
    TIMEOUT = auto()

    def __str__(self) -> str:
        """Return human-readable string representation."""
        return self.name.replace("_", " ").capitalize()
