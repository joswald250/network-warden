import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import subprocess

def get_csv():
    """Establish connection with raspi and pull csv"""

    remote_file_location = "pi@192.168.0.38:/home/pi/speedtest/speedtest.csv"
    command = ["scp", remote_file_location, "/home/joey/Documents/Raspi/Speedtest"]
    subprocess.run(command)

def panda_csv():
    """ Get data from csv """

    local_csv_location = "/home/joey/Documents/Raspi/network_warden/network_warden/data/speedtest.csv"
    columns = ["DateTime", "Ping (ms)", "Jitter (ms)", "Download (Mbps)", "Upload (Mbps)"]
    df = pd.read_csv(local_csv_location, usecols=columns)
    return df

def convert_to_np_array(df):
    "Converts what it expects to be a pandas dataframe (but an be anything) into a numpy array"

    np_array = np.asarray(df)
    return np_array

def my_plotter(data1, data2, param_dict={}, xlabel='', ylabel='', title=''):
    """ A helper function to make a single graph """

    fig, ax = plt.subplots()
    
    ax.set_xlabel(str(xlabel))
    ax.set_ylabel(str(ylabel))
    ax.set_title(str(title))
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.tick_params(axis='x', rotation=45)
    
    out = ax.plot(data1, data2, **param_dict)

    return out