from muddy.models import IPVersion

def get_ipversion_string(ip_version)
    if ip_version is IPVersion.IPV4:
        return 'ipv4'
    if ip_version is IPVersion.IPV6:
        return 'ipv6'
    
    raise InputException('ip_version is not valid: {ip_version}')