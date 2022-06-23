from pathlib import Path

import tomli
import tomli_w


"""
A series of functions used throughout the package as "helpers", or 
functions which will be reused in various modules.
"""

def read_from_config():
    """Pulls settings from config.toml.

    :return: contains all settings from config.toml in nested
        dictionary.
    :rtype: Python dictionary
    """
    
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "rb") as f:
        toml_dict = tomli.load(f)
    
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
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "wb") as f:
        tomli_w.dump(current_config, f)
