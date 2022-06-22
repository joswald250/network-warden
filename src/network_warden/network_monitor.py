import os
import re
import datetime
import subprocess

def main():
    """
    Gets network speed information from Speedtest CLI by Ookla
    
    Create a subprocess that launches a call to the Speedtest CLI and tells
    it to pipe everything from speedtest to stdout. Then creates variables from this
    readout and uses re package to filter. Inputs all data to a csv file, 'a+' tells 
    open function to append and create file if nonexistent.
    """

    response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', 
                                shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
    download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
    upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
    jitter = re.search('\((.*?)\s.+jitter\)\s', response, re.MULTILINE)

    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    jitter = jitter.group(1)
    
    try:
        f = open('/home/pi/network_monitor/network_monitor.csv', 'a+')
        if os.stat('/home/pi/network_monitor/network_monitor.csv').st_size == 0:
                f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
    except:
        pass
    
    now = datetime.datetime.now()
    f.write('{},{},{},{},{},{}\r\n'.format(now.strftime('%m/%d/%y'), now.strftime('%H:%M'), 
            ping, jitter, download, upload))

if __name__ == '__main__':
    main()