import random
import re
from datetime import datetime
import json

from overload import overload

from muddy.constants import DOMAIN_NAME_REGEX, HTTP_URL_REGEX, URN_URL_REGEX
from muddy.exceptions import InputException
from muddy.models import MatchType, IPVersion, Protocol, Direction
from muddy.utils import (
    get_ipversion_string, get_ipversion_suffix_string, get_sub_ace_name,
    get_ace_name, get_protocol_direction_suffix_string, get_policy_type_prefix_string
)


def make_support_info(mud_version: int, mud_url: str, is_supported: bool, cache_validity: int = None,
                      system_info: str = None, documentation: str = None,
                      masa_server: str = None, mfg_name: str = None,
                      last_update: str = None, model_name: str = None,
                      firmware_rev: str = None, software_rev: str = None):
    """Function to generate the MUD Model Definitions for the Root "mud" Container,
       minus to-device-policy and from-device-policy Containers.

    Args:
        mud_version (int): This node specifies the integer version of the MUD specification.
        mud_url (str): This is the MUD URL associated with the entry found in a MUD file.
        cache_validity (int, optional): The information retrieved from the MUD server is valid for these
                              many hours, after which it should be refreshed.
        is_supported (bool): This boolean indicates whether or not the Thing is currently supported
                             by the manufacturer.
        system_info (str, optional): A UTF-8 description of this Thing.  This should be a brief description that may be
                           displayed to the user to determine whether to allow the Thing on the network.
        documentation (str, optional): This URI consists of a URL that points to documentation relating to
                             the device and the MUD file.
        masa_server (str, optional): MASA server
        mfg_name (str, optional): Manufacturer name, as described in the ietf-hardware YANG module.
        last_update (str, optional): This is intended to be when the current MUD file
                                            was generated.  MUD managers SHOULD NOT check
                                            for updates between this time plus cache validity.
        model_name (str, optional): Model name, as described in theietf-hardware YANG module.
        firmware_rev (str, optional): firmware-rev, as described in the ietf-hardware YANG module.
                                             Note that this field MUST NOT be included when the device can be
                                             updated but the MUD URL cannot.
        software_rev (str, optional): software-rev, as described in the ietf-hardware YANG module.
                                             Note that this field MUST NOT be included when the device can be
                                             updated but the MUD URL cannot.

    Returns:
        dict: A dictionary representing the Root "mud" Container, minus to-device-policy and from-device-policy
              Containers.

    """
    support_info = {'mud-version': mud_version, 'mud-url': mud_url, 'is-supported': is_supported}

    if mfg_name is not None:
        support_info['mfg-name'] = mfg_name
    if model_name is not None:
        support_info['model-name'] = model_name
    if masa_server is not None:
        support_info["masa-server"] = masa_server
    if firmware_rev is not None:
        support_info["firmware-rev"] = firmware_rev
    if software_rev is not None:
        support_info["software-rev"] = software_rev
    if documentation is not None:
        support_info['documentation'] = documentation
    if system_info is not None:
        support_info['systeminfo'] = system_info
    if cache_validity is not None:
        support_info['cache-validity'] = cache_validity

    support_info['last-update'] = last_update if last_update is not None else datetime.now().strftime(
        '%Y-%m-%dT%H:%M:%S%z')

    return support_info


def make_port_range(dir_init: Direction, source_port: int, destination_port: int):
    """Function to generate the port ranges for an ACL

    Args:
        dir_init (Direction): The direction for which the TCP connection was initiated.
                              `Direction.TO_DEVICE` for Remote, `Direction.FROM_DEVICE` for Thing,
                              None for Either.
        source_port (int): The source port for the range. None for ANY.
        destination_port (int): The destination port for the range. None for ANY.

    Returns:
        dict: A dictionary representing the port range container.

    """
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


def make_acldns_match(domain: str, direction: Direction):
    """Function to generate an ACL match for a domain.

    Args:
        domain (str): The domain for this ACL
        direction (Direction): The direction for which the TCP connection was initiated.
                               `Direction.TO_DEVICE` for source domain, `Direction.FROM_DEVICE`
                               for destination domain.

    Returns:
        dict: A dictionary representing the ACLDNS match.

    """
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


def make_controller_match(url: str):
    """Function to generate an ACL match for classes of devices that are known to be controllers

    Args:
        url (str): URI for the device class

    Returns:
        dict: A dictionary representing the controller match.

    """
    if not (re.match(HTTP_URL_REGEX, url) or re.match(URN_URL_REGEX, url)):
        raise InputException('Not a valid URI: {}' % url)

    return {'controller': url}


def make_my_controller_match():
    """Function to generate an ACL match for access to controllers specific to this device

    Returns:
        dict: A dictionary representing the my-controller match.

    """
    return {'my-controller': []}


def make_manufacturer_match(domain: str):
    """Function to generate an ACL match for access to named manufacturers of devices that
       are identified by the domain names in their MUD URLs

    Args:
        domain (str): domain name for manufacturer

    Returns:
        dict: A dictionary representing the manufacturer match.

    """
    if not re.match(DOMAIN_NAME_REGEX, domain):
        raise InputException("Not a domain name: {domain}")

    return {'manufacturer': domain}


def make_same_manufacturer_match():
    """Function to generate an ACL match for access to devices to/from the same
       manufacturer based on the domain name in the MUD URL.

    Returns:
        dict: A dictionary representing the same-manufacturer match.

    """
    return {'same-manufacturer': []}


def make_sub_ace(sub_ace_name, protocol_direction, target_url, protocol, match_type,
                 direction_initiated, ip_version, local_port=None, remote_port=None):
    if len(target_url) > 140:
        raise InputException('target url is too long: {}' % target_url)
    match = {}

    ip_version = get_ipversion_string(ip_version)
    source_port = None
    destination_port = None
    cloud_ipv4_entry = None

    if match_type is MatchType.IS_CLOUD:
        cloud_ipv4_entry = make_acldns_match(target_url, protocol_direction)
    elif match_type is MatchType.IS_CONTROLLER:
        match['ietf-mud:mud'] = make_controller_match(target_url)
    elif match_type is MatchType.IS_MY_CONTROLLER:
        match['ietf-mud:mud'] = make_my_controller_match()
    elif match_type is MatchType.IS_MFG:
        match['ietf-mud:mud'] = make_manufacturer_match(target_url)
    elif match_type is MatchType.IS_MYMFG:
        match['ietf-mud:mud'] = make_same_manufacturer_match()

    if match.get('ietf-mud:mud') is None and cloud_ipv4_entry is None:
        raise InputException(f"match_type is not valid: {match_type}")

    if protocol is Protocol.ANY:
        if cloud_ipv4_entry:
            match[ip_version] = cloud_ipv4_entry
    else:
        if protocol_direction is Direction.FROM_DEVICE:
            source_port = remote_port
            destination_port = local_port
        elif protocol_direction is Direction.TO_DEVICE:
            source_port = local_port
            destination_port = remote_port
        if protocol is Protocol.TCP:
            match[ip_version] = {'protocol': 6}
            match['tcp'] = make_port_range(direction_initiated, source_port, destination_port)
        elif protocol is Protocol.UDP:
            match[ip_version] = {'protocol': 17}
        else:
            raise InputException(f'protocol is not valid: {protocol}')
        if cloud_ipv4_entry:
            match[ip_version].update(cloud_ipv4_entry)
    return {'name': sub_ace_name, 'matches': match, 'actions': {'forwarding': 'accept'}}


def make_ace(protocol_direction, target_url, protocol, match_types, direction_initiated, ip_version, local_ports=None,
             remote_ports=None):
    ace = []
    number_local_ports = len(local_ports) if type(local_ports) == list else 1
    number_remote_ports = len(remote_ports) if type(remote_ports) == list else 1
    for i in range(len(match_types)) if not isinstance(match_types, MatchType) else range(1):
        match_type = match_types[i] if not isinstance(match_types, MatchType) else match_types
        for l in range(number_local_ports):
            for r in range(number_remote_ports):
                ace.append(
                    make_sub_ace(
                        get_sub_ace_name(get_ace_name(match_type), direction_initiated, i + l + r),
                        protocol_direction,
                        target_url,
                        protocol, match_type, direction_initiated, ip_version,
                        local_ports[l] if local_ports is not None else None,
                        remote_ports[r] if remote_ports is not None else None
                    )
                )
    return ace


def make_acl(protocol_direction, ip_version, target_url, protocol, match_types,
             direction_initiated, local_ports=None, remote_ports=None, acl_name=None, mud_name=None):
    acl_type_prefix = get_ipversion_string(ip_version)
    if acl_name is None and mud_name is None:
        raise InputException('acl_name and mud_name can\'t both by None at the same time')
    elif acl_name is None:
        acl_name = make_acl_name(mud_name, ip_version, direction_initiated)
    return {'name': acl_name, 'type': acl_type_prefix,
            'aces': {
                'ace': make_ace(protocol_direction, target_url, protocol, match_types, direction_initiated, ip_version,
                                local_ports, remote_ports)}}


def make_acls(ip_version, target_url, protocol, match_types, direction_initiated, local_ports=None, remote_ports=None,
              acl_names=None, mud_name=None):
    acls = {}
    if acl_names is None and mud_name is None:
        raise InputException('acl_names and mud_name can\'t both by None at the same time')
    elif acl_names is None:
        acl_names = make_acl_names(mud_name, ip_version, direction_initiated)
    if ip_version == [IPVersion.BOTH]:
        ip_version = [IPVersion.IPV4, IPVersion.IPV6]
    for i in range(len(acl_names)):
        for protocol_direction in [Direction.TO_DEVICE, Direction.FROM_DEVICE]:
            acls.update(
                make_acl(protocol_direction, ip_version[i], target_url, protocol, match_types, direction_initiated,
                         local_ports, remote_ports, acl_names[i]))
    return acls


def make_acl_name(mud_name, ip_version, direction_initiated):
    acl_name_suffix_ip_version = get_ipversion_suffix_string(ip_version)
    acl_name_suffix_protocol_direction = get_protocol_direction_suffix_string(direction_initiated)

    return f"{mud_name}{acl_name_suffix_ip_version}{acl_name_suffix_protocol_direction}"


def make_acl_names(mud_name, ip_version, direction_initiated):
    acl_names = []
    if ip_version is IPVersion.BOTH:
        acl_names.append(make_acl_name(mud_name, IPVersion.IPV4, direction_initiated))
        acl_names.append(make_acl_name(mud_name, IPVersion.IPV6, direction_initiated))
    else:
        acl_names.append(make_acl_name(mud_name, ip_version, direction_initiated))
    return acl_names


def make_policy(direction_initiated, acl_names):
    policy_type_prefix = get_policy_type_prefix_string(direction_initiated)
    access_list = [{'name': name} for name in acl_names]
    return {
        f"{policy_type_prefix}-device-policy": {'access-lists': {'access-list': access_list}}
    }


@overload
def make_mud(mud_version, mud_url, is_supported, directions_initiated, ip_version, target_url, protocol, match_types,
             system_info=None, cache_validity=None, documentation=None, local_ports=None, remote_ports=None,
             masa_server=None, mfg_name=None, last_update=None, model_name=None):
    mud_name = f'mud-{random.randint(10000, 99999)}'
    acl = []
    policies = {}
    for direction_initiated in directions_initiated:
        acl_names = make_acl_names(mud_name, ip_version, direction_initiated)
        policies.update(make_policy(direction_initiated, acl_names))
        acl.append(
            make_acls([ip_version], target_url, protocol, match_types, direction_initiated, local_ports, remote_ports,
                      acl_names))
    mud = make_support_info(mud_version, mud_url, is_supported, cache_validity, system_info, documentation, masa_server,
                            mfg_name, last_update, model_name)
    mud.update(policies)
    return {'ietf-mud:mud': mud, 'ietf-access-control-list:acls': {'acl': acl}}


@make_mud.add
def make_mud_2(support_info, directions_initiated, ip_version: IPVersion, target_url, protocol, match_types,
               local_ports=None, remote_ports=None):
    acl = []
    policies = {}
    mud_name = f'mud-{random.randint(10000, 99999)}'
    for direction_initiated in directions_initiated:
        acl_names = make_acl_names(mud_name, ip_version, direction_initiated)
        policies.update(make_policy(direction_initiated, acl_names))
        acl.append(
            make_acls([ip_version], target_url, protocol, match_types, direction_initiated, local_ports, remote_ports,
                      acl_names))
    mud = support_info
    mud.update(policies)
    return {'ietf-mud:mud': mud, 'ietf-access-control-list:acls': {'acl': acl}}


@make_mud.add
def make_mud_3(policies, acls, mud_version, mud_url, is_supported, cache_validity=None, system_info=None,
               documentation=None, masa_server=None, mfg_name=None, last_update=None, model_name=None):
    mud = make_support_info(mud_version, mud_url, is_supported, cache_validity, system_info, documentation, masa_server,
                            mfg_name, last_update, model_name)
    mud.update(policies)
    return {'ietf-mud:mud': mud, 'ietf-access-control-list:acls': {'acl': acls}}


@make_mud.add
def make_mud_4(support_info, policies, acls):
    mud = support_info
    mud.update(policies)
    return {'ietf-mud:mud': mud, 'ietf-access-control-list:acls': {'acl': acls}}
