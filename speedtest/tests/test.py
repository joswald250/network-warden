import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

def panda_csv():
    """ Get data from csv """

    columns = ["DateTime", "Ping (ms)", "Jitter (ms)", "Download (Mbps)", "Upload (Mbps)"]
    df = pd.read_csv("/home/joey/Documents/Raspi/Speedtest/speedtest.csv", usecols=columns)
    return df

def convert_to_np_array(df):
    np_array = np.asarray(df)
    return np_array

def my_plotter(ax, data1, data2, param_dict={}, xlabel='', ylabel='', title=''):
    """ A helper function to make a graph """
    
    ax.set_xlabel(str(xlabel))
    ax.set_ylabel(str(ylabel))
    ax.set_title(str(title))
    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.tick_params(axis='x', rotation=45)
    
    out = ax.plot(data1, data2, **param_dict)
    ax.legend(ylabel)
    return out

def graph(data):
    """ Pull data columns into individual variables, access columns with numpy indices """
    
    datetime = data[:,0]
    ping = data[:,1]
    jitter = data[:,2]
    download = data[:,3]
    upload = data[:,4]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 9))

    my_plotter(ax1, datetime, jitter, xlabel='Time', ylabel='Rate (ms)', title='Network Jitter')
    my_plotter(ax2, datetime, upload, xlabel='Time', ylabel='Rate (Mbps)')
    my_plotter(ax2, datetime, download, xlabel='Time', ylabel='Rate (Mbps)', title='Network Download and Upload Speeds')
    

    '''ax.set_xlabel("Time")
    ax.set_ylabel("Rate")
    ax.set_title("Network Data over Time")
    ax.locator_params(axis='x', nbins=6)
      
    ax.plot(datetime, download, label="Download(Mbps)")
    ax.plot(datetime, upload, label="Upload (Mbps)")
    #ax.plot(datetime, ping, label="Ping (ms)")
    ax.plot(datetime, jitter, label="Jitter (ms)")'''
    
        #must put legend after labels in the plot functions above

    plt.show()


def main():
    df = panda_csv()
    data = convert_to_np_array(df)
    graph(data)

if __name__ == '__main__':
    main()