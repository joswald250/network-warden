from helpers import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Graph():
    """
    
    """

    jitter_graph_params = {"xlabel": "Time", "ylabel": "Jitter (ms)", "title": "Jitter over Time"}
    upload_graph_params = {"xlabel": "Time", "ylabel": "Upload (Mbps)", "title": "Upload Speed over Time"}
    download_graph_params = {"xlabel": "Time", "ylabel": "Download (Mbps)", "title": "Download Speed over Time"}

    def __init__(self, jitter=False, upload=False, download=False):
        """
        
        """
        
        self.jitter = jitter
        self.upload = upload
        self.download = download

        data = self.prepare_data()
        self.datetime = data[:,0]
        self.ping = data[:,1]
        self.jitter_data = data[:,2]
        self.download_data = data[:,3]
        self.upload_data = data[:,4]

        self.graph_selector()

    def graph_selector(self):
        """
        
        """
        
        if self.jitter and not self.upload and not self.download:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.datetime, self.jitter_data, self.jitter_graph_params)
        
        elif self.upload and not self.jitter and not self.download:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.datetime, self.upload_data, self.upload_graph_params)
        
        elif self.download and not self.jitter and not self.upload:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.datetime, self.download_data, self.download_graph_params)
        
        elif self.upload and self.jitter and not self.download:
            self.fig, self.axs = plt.subplots(2, sharex=True)
            self.my_plotter(self.axs[0], self.datetime, self.jitter_data, self.jitter_graph_params)
            self.my_plotter(self.axs[1], self.datetime, self.upload_data, self.upload_graph_params)

        elif self.download and self.jitter and not self.upload:
            self.fig, self.axs = plt.subplots(2, sharex=True)
            self.my_plotter(self.axs[0], self.datetime, self.jitter_data, self.jitter_graph_params)
            self.my_plotter(self.axs[1], self.datetime, self.download_data, self.download_graph_params)
        
        elif self.upload and self.download and not self.jitter:
            self.fig, self.axs = plt.subplots(2, sharex=True, sharey=True)
            self.my_plotter(self.axs[0], self.datetime, self.upload_data, self.upload_graph_params)
            self.my_plotter(self.axs[1], self.datetime, self.download_data, self.download_graph_params)
        
        elif self.upload and self.download and self.jitter:
            self.fig, self.axs = plt.subplots(3, sharex=True)
            self.my_plotter(self.axs[0], self.datetime, self.upload_data, self.upload_graph_params)
            self.my_plotter(self.axs[1], self.datetime, self.download_data, self.download_graph_params)
            self.my_plotter(self.axs[2], self.datetime, self.jitter_data, self.jitter_graph_params)

        else:
            Exception("graph_selector chose a non-possible option!")

        self.fig.set_figheight(7)
        self.fig.set_figwidth(10)
        plt.subplots_adjust(hspace=.5)
        plt.show()

    def prepare_data(self):
        """
        Calls three helper functions and returns a Numpy array object 
        containing the network data.
        """
        
        get_csv()
        df = panda_csv()
        data = convert_to_np_array(df)
        return data

    def my_plotter(self, ax, data1, data2, param_dict={}):
        """ A helper function to make a single graph """
        
        ax.set_xlabel(param_dict['xlabel'])
        ax.set_ylabel(param_dict['ylabel'])
        ax.set_title(param_dict['title'])
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.tick_params(axis='x', rotation=30)
        
        out = ax.plot(data1, data2)

        return out


def main(jitter=False, upload=False, download=False):
    """
    Function instantiates the Graph class and returns an instance of this class.

    Function requires one of three keywords (or any combination of these three)
    passed as True: 'jitter', 'upload', or 'download'. Each keyword, when passed, 
    will return a Graph instance of that particular variable. If multiple keywords 
    are passed, multiple instances are returned as a tuple. 
    For instance, if you call main('jitter=True', 'upload=True'), a tuple with two Graph 
    instances will be returned.

    A Graph instance is just a 
    """
    
    graph = Graph(jitter, upload, download)
    return graph

if __name__ == '__main__':
    main(upload=True, jitter=True, download=True)