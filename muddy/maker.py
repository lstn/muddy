from pprint import pprint

def make_support_info(mud_version, mud_url, last_update, cache_validity, 
        is_supported, masa_server, system_info, mfg_name, documentation, model_name):
        support_info = {}

        # if mfg_name is not None:
        #     support_info["mfg-name"]

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
    pprint(make_port_range("to-device", 888, 80))