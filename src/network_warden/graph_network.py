from helpers import *
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


def graph(data):
    """ Pull data columns into individual variables """
    
    datetime = data[:,0]
    ping = data[:,1]
    jitter = data[:,2]
    download = data[:,3]
    upload = data[:,4]
    
    
    my_plotter(datetime, jitter, xlabel='Time', ylabel='Jitter (ms)', title='Jitter over Time')
    
    
    plt.legend()    #must put legend after labels in the plot functions above
    
    plt.show()


def main():
    matplotlib.use('TkAgg')
    get_csv()
    df = panda_csv()
    data = convert_to_np_array(df)
    graph(data)

if __name__ == '__main__':
    main()