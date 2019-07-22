from muddy.models import IPVersion, Direction, MatchType, Protocol
from muddy.exceptions import InputException


def get_ipversion_string(ip_version):
    if ip_version is IPVersion.IPV4:
        return 'ipv4'
    if ip_version is IPVersion.IPV6:
        return 'ipv6'

    raise InputException(f'ip_version is not valid: {ip_version}')


def get_ipversion_suffix_string(ip_version):
    if ip_version is IPVersion.IPV4:
        return '-v4'
    if ip_version is IPVersion.IPV6:
        return '-v6'

    raise InputException(f'ip_version is not valid: {ip_version}')


def get_protocol_direction_suffix_string(direction):
    if direction is Direction.TO_DEVICE:
        return 'to'
    if direction is Direction.FROM_DEVICE:
        return 'fr'

    raise InputException(f'protocol_direction is not valid: {direction}')


def get_policy_type_prefix_string(direction):
    if direction is Direction.TO_DEVICE:
        return 'to'
    elif direction is Direction.FROM_DEVICE:
        return 'from'

    raise InputException(f'direction is not valid: {direction}')


def get_ace_name(match_type):
    if match_type is MatchType.IS_CLOUD:
        return 'cl'
    if match_type is MatchType.IS_MYMFG:
        return 'myman'
    if match_type is MatchType.IS_MFG:
        return 'man'
    if match_type is MatchType.IS_MY_CONTROLLER:
        return 'myctl'
    if match_type is MatchType.IS_CONTROLLER:
        return 'ent'

    raise InputException(f'match_type is not valid: {match_type}')


def get_sub_ace_name(ace_name, direction, sub_ace_number):
    if direction is Direction.TO_DEVICE:
        return f"{ace_name}{sub_ace_number}-todev"
    if direction is Direction.FROM_DEVICE:
        return f"{ace_name}{sub_ace_number}-frdev"
    raise InputException(f'direction is not valid: {direction}')


def get_ipversion_object(ip_version):
    if ip_version == 'ipv4':
        return IPVersion.IPV4
    if ip_version == 'ipv6':
        return IPVersion.IPV4
    if ip_version == 'both':
        return IPVersion.BOTH
    raise InputException(f'ip_version is not valid: {ip_version}')


def get_protocol_object(protocol):
    if protocol == 'udp':
        return Protocol.UDP
    if protocol == 'tcp':
        return Protocol.TCP
    if protocol == 'any':
        return Protocol.ANY
    raise InputException(f'protocol is not valid: {protocol}')


def get_direction_object(direction):
    if direction == 'to_device':
        return Direction.TO_DEVICE
    if direction == 'from_device':
        return Direction.FROM_DEVICE
    raise InputException(f'direction is not valid: {direction}')


def get_match_type_object(match_type):
    if match_type == 'is_my_controller':
        return MatchType.IS_MY_CONTROLLER
    if match_type == 'is_controller':
        return MatchType.IS_CONTROLLER
    if match_type == 'is_mfg':
        return MatchType.IS_MFG
    if match_type == 'is_mymfg':
        return MatchType.IS_MYMFG
    if match_type == 'is_cloud':
        return MatchType.IS_CLOUD
    raise InputException(f'match_type is not valid: {match_type}')
