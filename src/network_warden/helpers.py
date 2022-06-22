import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
import numpy as np
import pandas as pd
import subprocess
import tomli
import tomli_w


"""
A series of functions used throughout the package as "helpers", or 
functions which I could not find a better place to store.
"""

def get_csv():
    """Establish connection with raspi and pull csv, returns NoneType"""

    file_path = Path.cwd()
    remote_file_location = "pi@192.168.0.38:/home/pi/network_monitor/network_monitor.csv"
    local_file_location = file_path.joinpath('data', 'network_monitor.csv')
    command = ["scp", remote_file_location, local_file_location]
    subprocess.run(command)

def panda_csv():
    """ Get data from csv, validate it, return dataframe """

    file_path = Path.cwd()
    local_file_location = file_path.joinpath('data', 'network_monitor.csv')
    columns = ["Time", "Ping (ms)", "Jitter (ms)", "Download (Mbps)", "Upload (Mbps)"]
    df = pd.read_csv(local_file_location, usecols=columns)

    df = df.reset_index()

    rows_to_drop = []
    drop_criteria = ['FAILED']
    i = 0
    j = 0
    for i in range(0, len(df)):
        for j in range(0, len(df.columns)):
            if df.iloc[i, j] in drop_criteria:
                rows_to_drop.append(i)
                
    df = df.drop(rows_to_drop)

    t = 0
    for column in df.columns[2:]:
        df[column] = df[column].astype(float)

    return df

def convert_to_np_array(df):
    "Accepts anything that can be turned into an array and returns a numpy array"

    np_array = np.asarray(df)
    return np_array

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
