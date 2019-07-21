from enum import Enum, auto


class MatchType(Enum):
    """Enum class for ACL Match types
    """

    IS_LOCAL = auto()
    """Access to/from any local host for specific services (like COAP or HTTP)"""
    IS_MFG = auto()
    """Access to  of devices that are identified by the domain names in their MUD URLs"""
    IS_CONTROLLER = auto()
    """Access to classes of devices that are known to be controllers.
       Use this when you want different types of devices to access the same controller.	"""
    IS_CLOUD = auto()
    """ACLDNS Match Type
    """
    IS_MY_CONTROLLER = auto()
    """Access to controllers specific to this device (no need to name a class).   This is "my-controller".	"""
    IS_MYMFG = auto()
    """Access to devices to/from the same manufacturer based on the domain name in the MUD URL."""


class IPVersion(Enum):
    """Enum class for IP Versions
    """
    IPV4 = auto()
    IPV6 = auto()
    BOTH = auto()


class Protocol(Enum):
    """Enum class for Protocols
    """
    TCP = auto()
    UDP = auto()
    ANY = auto()


class Direction(Enum):
    """Enum class for Protocol directions (`from-device`, `to-device`)
    """
    TO_DEVICE = auto()
    FROM_DEVICE = auto()
