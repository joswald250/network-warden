from pathlib import Path

import tomli
import tomli_w


"""
A series of functions used throughout the package as "helpers", or 
functions which will be reused in various modules.
"""

def read_from_config():
    """Pulls settings from config.toml.

    Returns:
        Python dictionary: contains all settings from config.toml in nested
        dictionary.
    """
    
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "rb") as f:
        toml_dict = tomli.load(f)
    
    return toml_dict

def edit_config(section, key, new_value):
    """Edits the config.toml file.

    Args:
        section (string): string that should match the section of the 
        config.toml file.
        key (string): string of name of setting
        new_value (string): new value for setting
    """
    
    current_config = read_from_config()
    current_config[section][key] = new_value
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "wb") as f:
        tomli_w.dump(current_config, f)
