import subprocess

def get_csv():
    """Establish connection with raspi"""

    file_location = "pi@192.168.0.38:/home/pi/speedtest/speedtest.csv"
    command = ["scp", file_location, "/home/joey/Documents/Raspi/Speedtest"]
    subprocess.run(command)