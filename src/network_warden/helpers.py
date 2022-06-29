"""This module intends to simply hold a series of functions which will be
used throughout the package, and thus make more sense to store in a 
separate module than to re-write in multiple locations.

    :return: Nothing for the module itself - see function definitions for \
    more details on each individual function.
    :rtype: None
"""

from pathlib import Path

import tomli
import tomli_w


def read_from_config():
    """Pulls settings from config.toml.

    :return: contains all settings from config.toml in nested
        dictionary.
    :rtype: Python dictionary
    """
    
    try:
        p = Path(__file__).parent.resolve()
        with open(str(p) + "/config.toml", "rb") as f:
            toml_dict = tomli.load(f)
            return toml_dict
        
    except FileNotFoundError as error:
        print(error)
        print("Could not find file: config.toml, while executing " + __name__
            + ". Using default config.toml.")
        toml_dict = build_default_config()
        return toml_dict        

def edit_config(section, key, new_value):
    """Edits the config.toml file.

    :param section: string that should match the section of the 
        config.toml file.
    :type section: string
    :param key: string of name of setting
    :type key: string
    :param new_value: new value for setting
    :type new_value: string
    """
    
    current_config = read_from_config()
    current_config[section][key] = new_value
    p = Path(__file__).parent.resolve()
    with open(str(p) + "/config.toml", "wb") as f:
        tomli_w.dump(current_config, f)

def build_default_config():
    """Writes default configuration file to config.toml location.

    :return: Default configuration as a nested dictionary
    :rtype: Python dictionary
    """
    default_config = {
        "user": {
            "username": "joswald",
            "ip_address": "192.168.0.24",
            "remote_server_capability": "true",
            "csv_location": "/home/joey/network_monitor/network_monitor.csv"},
        "remote_servers": {
            "username": "pi",
            "ip_address": "192.168.0.38",
            "security_key": "",
            "csv_location": "/home/pi/network_monitor/network_monitor.csv"}}
    p = Path(__file__).parent.resolve()
    with open(str(p) + "/config.toml", "xb") as f:
        tomli_w.dump(default_config, f)
        
    return default_config