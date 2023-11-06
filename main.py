import datetime
import pytz
import holidays
import docker

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

    # Weekdays between midnight to 2pm
    if now.weekday() < 4 and now.hour >= 0 < 13:
        return False
    # Weekends between 4am to 7am
    elif now.weekday() >= 4 and now.hour >= 4 < 7:
        return False
    # Holidays between 4am to 7am
    elif is_holiday() and now.hour >= 4 < 7:
        return False
    # Times to turn on the server

    # Weekdays from 2pm to midnight
    elif now.weekday() < 4 and now.hour >= 13 < 24:
        return True
    # Weekdays from 7am to 4am
    elif now.weekday() >= 4 and now.hour >= 7 < 24:
        return True
    # Holidays between 7am to 4am
    elif is_holiday() and now.hour >= 7 < 24:
        return True
    else:
        return False


try:
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