from pprint import pprint
from datetime import datetime

def make_support_info(mud_version, mud_url, last_update, cache_validity, 
        is_supported, masa_server, system_info, mfg_name, documentation, model_name):
    support_info = {}

    if mfg_name is not None:
        support_info["mfg-name"] = mfg_name
    if model_name is not None:
        support_info["model-name"] = model_name
    if masa_server is not None:
        support_info["masa-server"] = masa_server
    
    support_info["mud-version"] = int(mud_version)
    support_info["mud-url"] = mud_url
    support_info["last-update"] = last_update if last_update is not None else datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
    support_info["cache-validity"] = int(cache_validity)
    support_info["is-supported"] = is_supported
    support_info["systeminfo"] = system_info
    support_info["documentation"] = documentation

    return support_info

def make_port_range(dir_init, source_port, destination_port):
    port_range = {}

    if dir_init is not None and dir_init in ["to-device", "from-device"]:
        port_range["ietf-mud:direction-initiated"] = dir_init

    if source_port is not None:
        port_range["source-port"] = {
            "operator": "eq",
            "port": int(source_port)
        }
    if destination_port is not None:
        port_range["destination-port"] = {
            "operator": "eq",
            "port": int(destination_port)
        }
    
    return port_range

if __name__ == "__main__":
    pprint(make_support_info(1, "https://test/123", None, 48, True, None, "aa", "CIRA", "https://doc.ca", "123"))
    pprint(make_support_info(1, "https://test/123", None, 48, True, None, "aa", None, "https://doc.ca", "123"))
    pprint(make_port_range("to-device", 888, 80))