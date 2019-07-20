from muddy.models import IPVersion, Direction
from muddy.exceptions import InputException


def get_ipversion_string(ip_version):
    if ip_version is IPVersion.IPV4:
        return 'ipv4'
    if ip_version is IPVersion.IPV6:
        return 'ipv6'

    raise InputException('ip_version is not valid: {ip_version}')

def get_sub_ace_name(ace_name, direction):
    if direction is Direction.TO_DEVICE:
        return f"{ace_name}{'{}'}-todev"
    if direction is Direction.FROM_DEVICE:
        return f"{ace_name}{'{}'}-frdev"
