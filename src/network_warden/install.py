"""Installs the crontab file that will run network monitor.
"""

from pathlib import Path
import subprocess

import helpers


class install():
    """Class that wraps methods for installing the crontab file for network
    monitor.py.
    """
    
    ip_address = "192.168.0.2"
    csv_file_location = "/home/pi/network_warden/network_monitor.csv"
    
    def __init__(self):
        """Loads settings and installs crontab.
        """

        self.load_settings()
        self.install_crontab()
        
    def load_settings(self):
        """Pulls module level settings from config.toml        
        """
        
        self.configs = helpers.read_from_config()
        remote_server_capability = self.configs["user"]["remote_server_capability"]
        if remote_server_capability:
            self.csv_file_location = self.configs["remote_servers"]["csv_location"]
            self.ip_address = self.configs["remote_servers"]["ip_address"]
        else:
            self.csv_file_location = self.configs["user"]["csv_location"]
            self.ip_address = self.configs["user"]["ip_address"]
    
    def install_crontab(self):
        """If present, it erases the previous crontab file in the cron.d 
        directory. It then creates a new one and writes to it.
        """
        
        path = Path('/etc/cron.d/network_monitor')
        
        rm_command = "rm /etc/cron.d/network_monitor"
        if path.is_file():
            subprocess.Popen(rm_command, shell=True, stdout=subprocess.PIPE)
        
        cwd = Path.cwd()
        crontab_path = Path.absolute(f"{cwd}/network_monitor.py")
        cron_text = f"# /etc/cron.d/network_monitor: crontab entries for the network warden package\n\nSHELL=/bin/sh\nPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n\n*/2 * * * * python3 {crontab_path}"
        install_command = "touch /etc/cron.d/network_monitor"
        subprocess.Popen(install_command, shell=True, stdout=subprocess.PIPE)
        crontab_path.write_text(cron_text)
        


def main():
    crontab = install()

if __name__ == '__main__':
    main()