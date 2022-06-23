import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import helpers

class Graph():
    """Gets and prepares data from a csv and then plots the requested graphs.

    Returns:
        Graph object: essentially a Matplotlib.Axes.Subplot object
    """

    jitter_graph_params = {"xlabel": "Time", "ylabel": "Jitter (ms)",
                            "title": "Jitter over Time"}
    upload_graph_params = {"xlabel": "Time", "ylabel": "Upload (Mbps)",
                            "title": "Upload Speed over Time"}
    download_graph_params = {"xlabel": "Time", "ylabel": "Download (Mbps)",
                            "title": "Download Speed over Time"}
    fig, axs = plt.subplots()
    ip_address = "192.168.0.2"
    csv_file_location = "/home/pi/network_monitor/network_monitor.csv"
    remote_server_capability = False
    remote_server_username = ""

    def __init__(self, jitter=False, upload=False, download=False):
        """Loads parameters and settings, then launches graph_selector().

        Args:
            jitter (bool, optional): Graph type. Defaults to False.
            upload (bool, optional): graph type. Defaults to False.
            download (bool, optional): graph type. Defaults to False.
        """
        
        self.jitter = jitter
        self.upload = upload
        self.download = download

        self.load_settings()

        data = self.prepare_data()
        self.time = data[:,1]
        self.ping = data[:,2]
        self.jitter_data = data[:,3]
        self.download_data = data[:,4]
        self.upload_data = data[:,5]

        self.graph_selector()

    def load_settings(self):
        """Pulls relevant config.toml settings.
        """
        configs = helpers.read_from_config()
        self.remote_server_capability = configs["user"]["remote_server_\
                                                            capability"]
        if self.remote_server_capability:
            self.csv_file_location = configs["remote_servers"]["csv_location"]
            self.ip_address = configs["remote_servers"]["ip_address"]
            self.remote_server_username = configs["remote_servers"]["username"]
        else:
            self.csv_file_location = configs["user"]["csv_location"]
            self.ip_address = configs["user"]["ip_address"]

    def graph_selector(self):
        """Based upon parameters passed to the __init__ function, returns an
        Axes.Subplot object(s).

        Returns:
            Graph object: Essentially a Matplotlib.Axes.Subplot object
        """
        
        if self.jitter and not self.upload and not self.download:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.time, self.jitter_data, 
                            self.jitter_graph_params)
        
        elif self.upload and not self.jitter and not self.download:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.time, self.upload_data, 
                            self.upload_graph_params)
        
        elif self.download and not self.jitter and not self.upload:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.time, self.download_data, 
                            self.download_graph_params)
        
        elif self.upload and self.jitter and not self.download:
            self.fig, self.axs = plt.subplots(2, sharex=True)
            self.my_plotter(self.axs[0], self.time, self.jitter_data, 
                            self.jitter_graph_params)
            self.my_plotter(self.axs[1], self.time, self.upload_data, 
                            self.upload_graph_params)

        elif self.download and self.jitter and not self.upload:
            self.fig, self.axs = plt.subplots(2, sharex=True)
            self.my_plotter(self.axs[0], self.time, self.jitter_data, 
                            self.jitter_graph_params)
            self.my_plotter(self.axs[1], self.time, self.download_data, 
                            self.download_graph_params)
        
        elif self.upload and self.download and not self.jitter:
            self.fig, self.axs = plt.subplots(2, sharex=True, sharey=True)
            self.my_plotter(self.axs[0], self.time, self.upload_data, 
                            self.upload_graph_params)
            self.my_plotter(self.axs[1], self.time, self.download_data, 
                            self.download_graph_params)
        
        elif self.upload and self.download and self.jitter:
            self.fig, self.axs = plt.subplots(3, sharex=True)
            self.my_plotter(self.axs[0], self.time, self.download_data, 
                            self.download_graph_params)
            self.my_plotter(self.axs[1], self.time, self.upload_data, 
                            self.upload_graph_params)
            self.my_plotter(self.axs[2], self.time, self.jitter_data, 
                            self.jitter_graph_params)

        else:
            Exception("graph_selector chose a non-possible option!")

        
        self.fig.set_figheight(7)
        self.fig.set_figwidth(10)
        plt.subplots_adjust(hspace=.5)

        return self.axs

    def prepare_data(self):
        """Calls three helper.py functions to prepare data for graphing.

        Returns:
            np.array: contains data to graph
        """
        
        if self.remote_server_capability:
            self.get_csv()
        
        df = self.panda_csv()
        data = self.convert_to_np_array(df)
        return data

    def my_plotter(self, ax, data1, data2, param_dict={}):
        """_summary_

        Args:
            ax (matplotlib.Axes): Axes object on which to add data
            data1 (np.array): can technically take any series/array object
            data2 (np.array): can technically take any series/array object
            param_dict (dict, optional): parameters accepted: xlabel, ylabel,
            title. Defaults to {}.

        Returns:
            matplotlib Line2D object: returns line for graph
        """
        
        ax.set_xlabel(param_dict['xlabel'])
        ax.set_ylabel(param_dict['ylabel'])
        ax.set_title(param_dict['title'])
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.tick_params(axis='x', rotation=30)
        
        out = ax.plot(data1, data2)

        return out

    def get_csv(self):
        """Establish connection with raspi and pull csv
        """

        file_path = Path.cwd()
        remote_file_location = self.remote_server_username + "@" + self.ip_address + ":" + self.csv_file_location
        local_file_location = file_path.joinpath('data', 'network_monitor.csv')
        command = ["scp", remote_file_location, local_file_location]
        subprocess.run(command)

    def panda_csv(self):
        """Gets data from local csv and validates it

        Returns:
            pd.Dataframe: dataframe containing validated csv data
        """

        file_path = Path.cwd()
        local_file_location = file_path.joinpath('data', 
                                                 'network_monitor.csv')
        columns = ["Time", "Ping (ms)", "Jitter (ms)", "Download (Mbps)", 
                   "Upload (Mbps)"]
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

    def convert_to_np_array(self, df):
        """Converts anything np.asarray accepts to a np.array

        Args:
            df (pd.Dataframe): expected, but not technically required

        Returns:
            np.array: NumPy Array object
        """

        np_array = np.asarray(df)
        return np_array

def main(jitter=False, upload=False, download=False):
    """Entry point for Graph class

    Args:
        jitter (bool, optional): graph type. Defaults to False.
        upload (bool, optional): graph type. Defaults to False.
        download (bool, optional): graph type. Defaults to False.

    Returns:
        Graph object: essentially a matplotlib.Axes.Subplot object
    """
    
    graph = Graph(jitter, upload, download)
    return graph

if __name__ == '__main__':
    main()