from get_csv.get_csv import get_csv
import matplotlib.pyplot as plt
import pandas as pd


def panda_csv():
    """ Get data from csv as panda dataframe """

    columns = ["DateTime", "Ping (ms)", "Jitter (ms)", "Download (Mbps)", "Upload (Mbps)"]
    df = pd.read_csv("/home/joey/Documents/Raspi/Speedtest/speedtest.csv", usecols=columns)
    return df

def graph(data):
    """ Pull data columns into individual variables """
    
    datetime = data['DateTime']
    ping = data['Ping (ms)']
    jitter = data['Jitter (ms)']
    download = data['Download (Mbps)']
    upload = data['Upload (Mbps)']
    
    """Format graph: note, figsize must go first"""
    plt.figure(figsize=(12,8))
    plt.xlabel("Time")
    plt.ylabel("Rate")
    plt.title("Network Data over Time")
    
    
    plt.plot(download, label="Download(Mbps)")
    plt.plot(upload, label="Upload (Mbps)")
    #plt.plot(ping, label="Ping (ms)")
    plt.plot(jitter, label="Jitter (ms)")
    
    plt.legend()    #must put legend after labels in the plot functions above
    
    plt.show()


def main():
    get_csv()
    data = panda_csv()
    graph(data)

if __name__ == '__main__':
    main()