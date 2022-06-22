from helpers import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Graph():
    """
    This class accepts parameters for the type of graph and returns a matplolib.Axes.Subplot
    object.

    Parameters expected: 'jitter', 'upload', 'download'

    Attributes: 
    - jitter_graph_params
    - upload_graph_params
    - download_graph_params
    - fig, axs for a subplot

    Methods:
    - __init__
    - graph_selector
    - prepare_data
    - my_plotter 
    """

    jitter_graph_params = {"xlabel": "Time", "ylabel": "Jitter (ms)", "title": "Jitter over Time"}
    upload_graph_params = {"xlabel": "Time", "ylabel": "Upload (Mbps)", "title": "Upload Speed over Time"}
    download_graph_params = {"xlabel": "Time", "ylabel": "Download (Mbps)", "title": "Download Speed over Time"}
    fig, axs = plt.subplots()

    def __init__(self, jitter=False, upload=False, download=False):
        """
        Accepts parameters for the type of graph, launches graph_selector function.

        Calls the prepare_data function and loads the relevant data variables
        for use throughout the class.
        """
        
        self.jitter = jitter
        self.upload = upload
        self.download = download

        data = self.prepare_data()
        self.time = data[:,1]
        self.ping = data[:,2]
        self.jitter_data = data[:,3]
        self.download_data = data[:,4]
        self.upload_data = data[:,5]

        self.graph_selector()

    def graph_selector(self):
        """
        Based upon parameters passed to the __init__ function, returns an
        Axes.Subplot object(s).

        Calls my_plotter function with parameters dependent upon the parameters
        passed in the __init__ function. Sets a few figure variables and then
        returns the Axes.Subplot object.
        """
        
        if self.jitter and not self.upload and not self.download:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.time, self.jitter_data, self.jitter_graph_params)
        
        elif self.upload and not self.jitter and not self.download:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.time, self.upload_data, self.upload_graph_params)
        
        elif self.download and not self.jitter and not self.upload:
            self.fig, self.ax = plt.subplots()
            self.my_plotter(self.ax, self.time, self.download_data, self.download_graph_params)
        
        elif self.upload and self.jitter and not self.download:
            self.fig, self.axs = plt.subplots(2, sharex=True)
            self.my_plotter(self.axs[0], self.time, self.jitter_data, self.jitter_graph_params)
            self.my_plotter(self.axs[1], self.time, self.upload_data, self.upload_graph_params)

        elif self.download and self.jitter and not self.upload:
            self.fig, self.axs = plt.subplots(2, sharex=True)
            self.my_plotter(self.axs[0], self.time, self.jitter_data, self.jitter_graph_params)
            self.my_plotter(self.axs[1], self.time, self.download_data, self.download_graph_params)
        
        elif self.upload and self.download and not self.jitter:
            self.fig, self.axs = plt.subplots(2, sharex=True, sharey=True)
            self.my_plotter(self.axs[0], self.time, self.upload_data, self.upload_graph_params)
            self.my_plotter(self.axs[1], self.time, self.download_data, self.download_graph_params)
        
        elif self.upload and self.download and self.jitter:
            self.fig, self.axs = plt.subplots(3, sharex=True)
            self.my_plotter(self.axs[0], self.time, self.download_data, self.download_graph_params)
            self.my_plotter(self.axs[1], self.time, self.upload_data, self.upload_graph_params)
            self.my_plotter(self.axs[2], self.time, self.jitter_data, self.jitter_graph_params)

        else:
            Exception("graph_selector chose a non-possible option!")

        
        self.fig.set_figheight(7)
        self.fig.set_figwidth(10)
        plt.subplots_adjust(hspace=.5)

        return self.axs

    def prepare_data(self):
        """
        Calls three helper,py functions and returns a Numpy array object 
        containing the network data.
        """
        
        get_csv()
        df = panda_csv()
        data = convert_to_np_array(df)
        return data

    def my_plotter(self, ax, data1, data2, param_dict={}):
        """
        Accepts an Axes object, x and y data, and a parameter dictionary,
        returns a Line2D object
        """
        
        ax.set_xlabel(param_dict['xlabel'])
        ax.set_ylabel(param_dict['ylabel'])
        ax.set_title(param_dict['title'])
        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.yaxis.set_major_locator(ticker.AutoLocator())
        ax.tick_params(axis='x', rotation=30)
        
        out = ax.plot(data1, data2)

        return out


def main(jitter=False, upload=False, download=False):
    """
    Function instantiates the Graph class and returns Graph object, which is 
    essentially an Axes.Subplot object.

    Function accepts one of three keywords (or any combination of these three)
    with a value of True: 'jitter', 'upload', or 'download'. 
    """
    
    graph = Graph(jitter, upload, download)
    return graph

if __name__ == '__main__':
    main(jitter=True)