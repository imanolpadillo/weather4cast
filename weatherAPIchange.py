import RPi.GPIO as GPIO
import threading
import time
import weather, max7219
from gpioenum import gpio
import wlogging
from wlogging import LogType, LogId


# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the pulse
PULSE_PIN = gpio.BUTTON_API_CHG.value

# Set up the GPIO pin as input
GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function to handle pulse detection
def pulse_detector():
    if GPIO.input(PULSE_PIN):
        if weather.api_weather_id == 1:
            weather.api_weather_id = 2
            max7219.message='A2'
        elif weather.api_weather_id == 2:
            weather.api_weather_id = 3
            max7219.message='A3'
        else:
            weather.api_weather_id = 1
            max7219.message='A1'
        log = 'API' + str(weather.api_weather_id)
        wlogging.log(LogType.INFO.value,LogId.API_CHG.value,log)
        time.sleep(3)
        return True
    else:
        return False



