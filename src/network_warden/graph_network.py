"""This module intends to wrap all functionality related to the actual
creation of graphs.

This includes gathering (either from a remote or local source) and preparing
all of the data necessary for creating these graphs. 

    :return: A Graph object that wraps a matplotlib figure and Axes object(s).
    :rtype: Graph object
"""

import subprocess
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import helpers

    
class Graph():
    """Interprets parameters and plots the requested graphs.

    :param jitter: graph type, defaults to False
    :type jitter: bool, optional
    :param upload: graph type, defaults to False
    :type upload: bool, optional
    :param download: graph type, defaults to False
    :type download: bool, optional
    :return: essentially a matplotlib.Axes.Subplot object
    :rtype: Graph object
    """
    
    
    jitter_graph_params = {"xlabel": "Time", "ylabel": "Jitter (ms)",
                            "title": "Jitter over Time"}
    upload_graph_params = {"xlabel": "Time", "ylabel": "Upload (Mbps)",
                            "title": "Upload Speed over Time"}
    download_graph_params = {"xlabel": "Time", "ylabel": "Download (Mbps)",
                            "title": "Download Speed over Time"}
    def __init__(self, jitter, upload, download):
        
        i = 0
        graphed = {}
        if jitter:
            graphed["jitter"] = False
            i += 1
        if upload:
            graphed["upload"] = False
            i += 1
        if download:
            graphed["download"] = False
            i += 1

        if len(graphed) == 0:
            message = "No graph type selected!"
            raise ValueError(message)
        
        data = LineData(jitter=jitter, upload=upload, download=download)
        print(data.x_tick_labels)
        
        fig, axs = plt.subplots(i, sharex=True)
        fig.set_size_inches(12, 9)
        
        plt.subplots_adjust(hspace=.3)
        
        # If more than one graph type requested, use the my_plotter function
        # to create the Line2D object, the 'graphed' dictionary keeps track
        # of which Line2D objects are already created. 
        if i > 1:
            for j in range(0, i):
                if jitter and graphed["jitter"] == False:
                    self.my_plotter(axs[j], data.time_data, data.jitter_data,
                                data.x_tick_labels, self.jitter_graph_params)
                    graphed["jitter"] = True
                    continue
                if upload and graphed["upload"] == False:
                    self.my_plotter(axs[j], data.time_data, data.upload_data,
                                data.x_tick_labels, self.upload_graph_params)
                    graphed["upload"] = True
                    continue
                if download and graphed["download"] == False:
                    self.my_plotter(axs[j], data.time_data, data.download_data,
                                data.x_tick_labels, self.download_graph_params)
                    graphed["download"] = True
        else:
        # If only one graph type requested - need separate clause because
        # cannot use index '[j]' on a single axes object.
            if jitter:
                    self.my_plotter(axs, data.time_data, data.jitter_data,
                                data.x_tick_labels, self.jitter_graph_params)
            if upload:
                self.my_plotter(axs, data.time_data, data.upload_data,
                            data.x_tick_labels, self.upload_graph_params)
            if download:
                self.my_plotter(axs, data.time_data, data.download_data,
                            data.x_tick_labels, self.download_graph_params)
    
    def my_plotter(self, ax, data1, data2, x_tick_labels, param_dict={}):
        """Creates a line based upon input x, y

        :param ax: Axes object on which to add data
        :type ax: matplotlib.Axes
        :param data1: can technically take any series/array object
        :type data1: np.array
        :param data2: can technically take any series/array object
        :type data2: np.array
        :param param_dict: parameters accepted: xlabel, ylabel,
            title. defaults to {}
        :type param_dict: dict, optional
        :return: returns line for graph
        :rtype: matplotlib Line2D object
        """
        
        ax.set_xlabel(param_dict['xlabel'])
        ax.set_ylabel(param_dict['ylabel'])
        ax.set_title(param_dict['title'])
        # ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.tick_params(axis='x', rotation=30)
        ax.set_xticklabels(x_tick_labels)
        
        out = ax.plot(data1, data2)

        return out

    


class LineData():
    """Returns four numpy arrays with the data to be graphed.
    
    This class takes input parameters, fetches data from remote source (if
    remote_server_capability equals True in config.toml), prepares it for
    graphing and then returns all the series as a single object.

    :return: LineData object which wraps all data together.
    :rtype: LineData object
    """
    
    
    time_data = []
    x_tick_labels= []
    jitter_data = []
    upload_data = []
    download_data = []
    
    def __init__(self, jitter=False, upload=False, download=False):
        """Loads parameters and settings, then launches graph_selector().

        :param jitter:Graph type, defaults to False
        :type jitter: bool, optional
        :param upload: Graph type, defaults to False
        :type upload: bool, optional
        :param download: Graph type, defaults to False
        :type download: bool, optional
        """
        
        self.jitter = jitter
        self.upload = upload
        self.download = download

        self.load_settings()

        data = self.prepare_data()
        self.time_data = data[:,1]
        # Convert timestamp to readable format
        self.x_tick_labels = self.timestamp_to_date_time(self.time_data)
        if self.jitter:
            self.jitter_data = data[:,3]
        if self.download:
            self.download_data = data[:,4]
        if self.upload:
            self.upload_data = data[:,5]
            
        
        
    def load_settings(self):
        """Pulls relevant config.toml settings.
        """
        configs = helpers.read_from_config()
        self.remote_server_capability = configs["user"]["remote_server_capability"]
        if self.remote_server_capability:
            self.csv_file_location = configs["remote_servers"]["csv_location"]
            self.ip_address = configs["remote_servers"]["ip_address"]
            self.remote_server_username = configs["remote_servers"]["username"]
        else:
            self.csv_file_location = configs["user"]["csv_location"]
            self.ip_address = configs["user"]["ip_address"]
    
    def prepare_data(self):
        """Calls three helper.py functions to prepare data for graphing.

        :return: contains data to graph
        :rtype: np.array
        """
        
        if self.remote_server_capability:
            self.get_csv()
        
        df = self.panda_csv()
        data = self.convert_to_np_array(df)
        return data
    
    def get_csv(self):
        """Establish connection with raspi and pull csv
        """

        file_path = Path.cwd()
        remote_file_location = (self.remote_server_username
        + "@" + self.ip_address + ":" + self.csv_file_location)
        local_file_location = file_path.joinpath('data', 'network_monitor.csv')
        command = ["scp", remote_file_location, local_file_location]
        try:
            subprocess.run(command)
        except ConnectionError as error:
            print(error)
            print("Connection error when attempting scp during function: "
                  + __name__ + ".")
        

    def panda_csv(self):
        """Gets data from local csv and validates it

        :return: dataframe containing validated csv data
        :rtype: pd.Dataframe
        """

        file_path = Path.cwd()
        local_file_location = file_path.joinpath('data', 
                                                 'network_monitor.csv')
        columns = ["Timestamp", "Latency (ms)", "Jitter (ms)", "Download (Mbps)", 
                   " Upload (Mbps)"]
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

        :param df: expected, but not technically required
        :type df: pd.Dataframe
        :return: NumPy Array object
        :rtype: np.array
        """

        np_array = np.asarray(df)
        return np_array
    
    def timestamp_to_date_time(self, series):
        date_time_array = np.array(series)
        str_array = []
        print(str_array)
        for i in range(0, len(date_time_array)):
            dto = datetime.fromtimestamp(date_time_array[i])
            print(dto)
            value = dto.strftime("%m-%d: %H:%M")
            print(value)
            str_array.append(value)
            print(str_array[i])
        str_array = np.asarray(str_array, dtype=str)
        return str_array
    
    

def main(jitter=False, upload=False, download=False):
    """Entry point for graph_network.py

    :param jitter: if True, will return jitter graph, defaults to False
    :type jitter: bool, optional
    :param upload: if True, will return upload graph, defaults to False
    :type upload: bool, optional
    :param download: if True, will return download graph, defaults to False
    :type download: bool, optional
    """
    
    
    
    graph = Graph(jitter, upload, download)
    return graph
        
    
if __name__ == '__main__':
    main()
