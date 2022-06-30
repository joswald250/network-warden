"""This module is the heart of the Network Warden project. It actually collects
and stores the data about the network performance.
"""

import os
import re
import datetime
import subprocess

import helpers


class Network_Monitor():
    """Contains the main function for monitoring the network and building 
    the csv file containing the data.
    """
    ip_address = "192.168.0.2"
    csv_file_location = "/home/pi/network_warden/network_monitor.csv"

    def __init__(self):
        """Loads settings and runs speedtest function.
        """

        self.load_settings()
        self.speedtest()

    def load_settings(self):
        """Pulls module level settings from config.toml        
        """

        configs = helpers.read_from_config()
        remote_server_capability = configs["user"]["remote_server_capability"]
        if remote_server_capability:
            self.csv_file_location = configs["remote_servers"]["csv_location"]
            self.ip_address = configs["remote_servers"]["ip_address"]
        else:
            self.csv_file_location = configs["user"]["csv_location"]
            self.ip_address = configs["user"]["ip_address"]
        

    def speedtest(self):
        """Gets network speed information from Speedtest CLI by Ookla
        
        Create a subprocess that launches a call to the Speedtest CLI and tells
        it to pipe everything from speedtest to stdout. Then creates variables 
        from this readout and uses 're' package to filter. Inputs all data to 
        a csv file, 'a+' tells open function to append and create file if 
        nonexistent.
        """
        command = '/usr/bin/speedtest --accept-license --accept-gdpr'
        response = subprocess.Popen(command, shell=True, 
                    stdout=subprocess.PIPE).stdout.read().decode('utf-8')

        latency = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
        download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
        upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
        jitter = re.search('\((.*?)\s.+jitter\)\s', response, re.MULTILINE)

        latency = latency.group(1)
        download = download.group(1)
        upload = upload.group(1)
        jitter = jitter.group(1)
        
        try:
            f = open(self.csv_file_location, 'a+')
            if os.stat(self.csv_file_location).st_size == 0:
                f.write('Timestamp,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
        except:
            pass
        
        now = datetime.datetime.now(datetime.timezone.utc)
        ts = datetime.datetime.timestamp(now)
        f.write('{},{},{},{},{}\r\n'.format(ts, latency, jitter, download, 
                                            upload))

def main():
    """Instantiates the Network_Monitor class.
    """
    net_mon = Network_Monitor()

if __name__ == '__main__':
    main()