from enum import Enum, auto


class MatchType(Enum):
    IS_LOCAL = auto()
    IS_MFG = auto()
    IS_CONTROLLER = auto()
    IS_CLOUD = auto()
    IS_MY_CONTROLLER = auto()
    IS_MYMFG = auto()


class IPVersion(Enum):
    IPV4 = auto()
    IPV6 = auto()
    BOTH = auto()


class Protocol(Enum):
    TCP = auto()
    UDP = auto()
    ANY = auto()


class Direction(Enum):
    TO_DEVICE = auto()
    FROM_DEVICE = auto()
