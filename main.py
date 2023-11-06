import datetime
import pytz
import holidays
import docker
import os
from rcon.source import Client
from dotenv import load_dotenv

load_dotenv()
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
RCON_PASSWORD = os.getenv('RCON_PASSWORD')


# Check current time
now = datetime.datetime.now(pytz.timezone('America/Boise'))
us_holidays = holidays.US()


# Check if it is a holiday
def is_holiday():
    if now.date() in us_holidays:
        return True
    else:
        return False


def online_schedule():
    # Times to turn off the server

    # Weekdays are Monday through Thursday

    # Weekdays between midnight to 1am
    if now.weekday() < 4 and now.hour >= 0 < 1:
        return False
    # Weekends between 4am to 7am
    elif now.weekday() >= 4 and now.hour >= 4 < 5:
        return False
    # Holidays between 4am to 7am
    elif is_holiday() and now.hour >= 4 < 7:
        return False
    # Times to turn on the server

    # Weekdays from 2pm to midnight
    elif now.weekday() < 4 and now.hour >= 14 < 24:
        return True
    # Weekdays from 7am to 4am
    elif now.weekday() >= 4 and now.hour >= 7 < 24:
        return True
    # Holidays between 7am to 4am
    elif is_holiday() and now.hour >= 7 < 24:
        return True
    else:
        return False


# Check if anyone is online
def is_anyone_online():
    with Client(SERVER_IP, SERVER_PORT, passwd=RCON_PASSWORD) as client:
        response = client.run('admincheet', 'listPlayers')
    if response == 'No Players Connected':
        return False
    else:
        return True


try:
    if is_anyone_online():
        print('Someone is online, not changing server status')
        exit()
    if online_schedule():
        # Docker client setup
        docker_client = docker.from_env()

        # Check if server is running
        container = docker_client.containers.get('ark-server')
        # If it is not running, start it.
        if container.status != 'running':
            print('Server is not running, starting now')
            container.start()
        else:
            print('Server is already running')
    else:
        docker_client = docker.from_env()

        # Check if server is running
        container = docker_client.containers.get('ark-server')
        # If it is running, stop it.
        if container.status == 'running':
            print('Server is running, stopping now')
            container.stop()
        else:
            print('Server is not running')
except Exception as e:
    print(e)