from pprint import pprint
from datetime import datetime
import re

from muddy.constants import DOMAIN_NAME_REGEX, HTTP_URL_REGEX, URN_URL_REGEX
from muddy.exceptions import InputException
from muddy.models import MatchType, IPVersion, Protocol, Direction
from muddy.utils import (
    get_ipversion_string, get_ipversion_suffix_string, get_sub_ace_name,
    get_ace_name, get_protocol_direction_suffix_string, get_policy_type_prefix_string
)


def make_support_info(mud_version, mud_url, last_update, cache_validity,
                      is_supported, masa_server, system_info, mfg_name, documentation, model_name):
    support_info = {}

    if mfg_name is not None:
        support_info['mfg-name'] = mfg_name
    if model_name is not None:
        support_info['model-name'] = model_name
    if masa_server is not None:
        support_info["masa-server"] = masa_server

    support_info['mud-version'] = int(mud_version)
    support_info['mud-url'] = mud_url
    support_info['last-update'] = last_update if last_update is not None else datetime.now().strftime(
        '%Y-%m-%dT%H:%M:%S%z')
    support_info['cache-validity'] = int(cache_validity)
    support_info['is-supported'] = is_supported
    support_info['systeminfo'] = system_info
    support_info['documentation'] = documentation

    return support_info


def make_port_range(dir_init, source_port, destination_port):
    port_range = {}

    if dir_init is not None and dir_init is Direction.TO_DEVICE:
        port_range['ietf-mud:direction-initiated'] = "to-device"
    if dir_init is not None and dir_init is Direction.FROM_DEVICE:
        port_range['ietf-mud:direction-initiated'] = "from-device"

    if source_port is not None:
        port_range['source-port'] = {
            'operator': 'eq',
            'port': int(source_port)
        }
    if destination_port is not None:
        port_range['destination-port'] = {
            'operator': 'eq',
            'port': int(destination_port)
        }

    return port_range


def make_acldns_match(domain, direction):
    if not re.match(DOMAIN_NAME_REGEX, domain):
        raise InputException(f"Not a domain name: {domain}")

    acldns_match = {}
    key = "ietf-acldns:src-dnsname" if direction is Direction.TO_DEVICE else \
        "ietf-acldns:dst-dnsname" if direction is Direction.FROM_DEVICE else None

    if key:
        acldns_match[key] = domain
    else:
        raise InputException(f"direction is not valid: {direction}")

    return acldns_match


def make_controller_match(url):
    if not (re.match(HTTP_URL_REGEX, url) or re.match(URN_URL_REGEX, url)):
        raise InputException('Not a valid URL: {}' % url)

    return {'controller', url}


def make_my_controller_match():
    return {'my-controller', [None]}


def make_manufacturer_match(domain):
    if not re.match(DOMAIN_NAME_REGEX, domain):
        raise InputException("Not a domain name: {domain}")

    return {'manufacturer': domain}


def make_same_manufacturer_match():
    return {'same-manufacturer', [None]}


def make_sub_ace(sub_ace_name, protocol_direction, target_url, protocol, local_port, remote_port, match_type,
                 direction_initiated, ip_version):
    if len(target_url) > 140:
        raise InputException('target url is to long: {}' % target_url)
    match = {}

    ip_version = get_ipversion_string(ip_version)
    source_port = None
    destination_port = None

    cloud_ipv4_entry = make_acldns_match(target_url, protocol_direction) if match_type is MatchType.IS_CLOUD else None
    match['ietf-mud:mud'] = make_controller_match(target_url) if match_type is MatchType.IS_CONTROLLER else None
    match['ietf-mud:mud'] = make_my_controller_match() if match_type is MatchType.IS_MY_CONTROLLER else None
    match['ietf-mud:mud'] = make_manufacturer_match(target_url) if match_type is MatchType.IS_MFG else None
    match['ietf-mud:mud'] = make_same_manufacturer_match() if match_type is MatchType.IS_MYMFG else None

    if match['ietf-mud:mud'] is None and not cloud_ipv4_entry:
        raise InputException(f"match_type is not valid: {match_type}")

    if protocol is Protocol.ANY and cloud_ipv4_entry:
        match['ipv4'] = cloud_ipv4_entry
    else:
        if protocol_direction is Direction.TO_DEVICE:
            source_port = remote_port
            destination_port = local_port
        elif protocol_direction is Direction.FROM_DEVICE:
            source_port = local_port
            destination_port = remote_port
        if protocol is Protocol.TCP:
            match['ipv4'] = {'protocol': 6}
            match['tcp'] = make_port_range(direction_initiated, source_port, destination_port)
        elif protocol is Protocol.UDP:
            match['ipv4'] = {'protocol': 17}
        else:
            raise InputException(f'protocol is not valid: {protocol}')
        if cloud_ipv4_entry:
            match[ip_version].update(cloud_ipv4_entry)
    return {'name': sub_ace_name, 'matches': match}


def make_ace(protocol_direction, target_url, protocol, local_ports, remote_ports, match_type,
             direction_initiateds, ip_version):
    ace = []
    ace_name = get_ace_name(match_type)
    sub_ace_name = get_sub_ace_name(ace_name, protocol_direction)

    for i in range(len(protocol)):
        ace.append(
            make_sub_ace(
                sub_ace_name.format(i), protocol_direction[i], target_url, protocol, local_ports[i],
                remote_ports[i], match_type, direction_initiateds, ip_version
            )
        )
    return ace


def make_acl(ip_version, protocol_direction, target_url, protocol, local_ports, remote_ports, match_type,
             direction_initiateds, acl_name=None, mud_name=None):
    acl_type_prefix = get_ipversion_string(ip_version)

    if acl_name is None and mud_name is None:
        raise InputException('acl_name and mud_name can\'t both by None at the same time')
    elif acl_name is None:
        acl_name = make_acl_name(mud_name, ip_version, protocol_direction)
    return {'name': acl_name, 'type': acl_type_prefix,
            'aces': {'ace': [make_ace(protocol_direction, target_url, protocol, local_ports, remote_ports, match_type,
                                      direction_initiateds, ip_version)]}}


def make_acl_name(mud_name, ip_version, protocol_direction):
    acl_name_suffix_ip_version = get_ipversion_suffix_string(ip_version)
    acl_name_suffix_protocol_direction = get_protocol_direction_suffix_string(protocol_direction)

    return f"{mud_name}{acl_name_suffix_ip_version}{acl_name_suffix_protocol_direction}"

def make_policy(protocol_direction, acl_names):
    policy_type_prefix = get_policy_type_prefix_string(protocol_direction)
    return {
        f"{policy_type_prefix}-device-policy": {'access-lists': {'access-list': acl_names}}
    }


if __name__ == '__main__':
    # pprint(make_support_info(1, 'https://test/123', None, 48, True, None, 'aa', 'CIRA', 'https://doc.ca', '123'))
    # pprint(make_support_info(1, 'https://test/123', None, 48, True, None, 'aa', None, 'https://doc.ca', '123'))
    # pprint(make_port_range('to-device', 888, 80))
    # pprint(
    #     make_sub_ace('ace', Direction.TO_DEVICE, 'www.google.com', Protocol.UDP, 888, 80, MatchType.IS_CLOUD,
    #                  'to-device', IPVersion.IPV4))
    pprint(
        make_ace('ace', Direction.TO_DEVICE, 'www.google.com', [Protocol.ANY], [888, 57], [80, 4],
                 MatchType.IS_CLOUD,
                 ['to-device', 'to-device'], IPVersion.IPV4))
