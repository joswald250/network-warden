from pathlib import Path
import tomli
import tomli_w


"""
A series of functions used throughout the package as "helpers", or 
functions which will be reused in various modules.
"""

def read_from_config():
    """
    Establishes the cwd with pathlib and returns a dictionary object
    with the current settings from the config.toml file.
    """
    
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "rb") as f:
        toml_dict = tomli.load(f)
    
    return toml_dict

def edit_config(section, key, new_value):
    """
    Accepts the section, key, and new value of each setting as parameters,
    then edits the config.toml file. Returns NoneType.
    """
    
    current_config = read_from_config()
    current_config[section][key] = new_value
    p = Path.cwd()
    with open(str(p) + "/src/network_warden/config.toml", "wb") as f:
        tomli_w.dump(current_config, f)
