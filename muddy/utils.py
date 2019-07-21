from muddy.models import IPVersion, Direction, MatchType
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


def get_sub_ace_name(ace_name, direction):
    if direction is Direction.TO_DEVICE:
        return f"{ace_name}{'{}'}-todev"
    if direction is Direction.FROM_DEVICE:
        return f"{ace_name}{'{}'}-frdev"
    raise InputException(f'direction is not valid: {direction}')
