import os
import re
import datetime
import subprocess

def main():
    """Create a subprocess that launches a call to the Speedtest CLI and tells
    it to pipe everything from speedtest to stdout"""

    response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', 
                                shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

    """Create several variables from the readout of the previous line"""

    ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
    download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
    upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
    jitter = re.search('\((.*?)\s.+jitter\)\s', response, re.MULTILINE)

    """Group is part of the re package and selects the first result from the search"""

    ping = ping.group(1)
    download = download.group(1)
    upload = upload.group(1)
    jitter = jitter.group(1)

    """A+ tells it to append, and create the file if nonexistent"""
    
    try:
        f = open('/home/pi/speedtest/speedtest.csv', 'a+')
        if os.stat('/home/pi/speedtest/speedtest.csv').st_size == 0:
                f.write('DateTime,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
    except:
        pass
    
    now = datetime.datetime.now()
    f.write('{},{},{},{},{}\r\n'.format(now.strftime('%m/%d/%y %H:%M'), 
            ping, jitter, download, upload))

if __name__ == '__main__':
    main()