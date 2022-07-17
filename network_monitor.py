# /etc/cron.d/network_monitor: crontab entries for the network warden package

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

*/2 * * * * python3 /home/joey/code/Raspi/network_warden/network_monitor.py