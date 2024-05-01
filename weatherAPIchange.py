# *************************************************************************************************** 
# ***************************************** WeatherAPIchange ****************************************
# *************************************************************************************************** 
import RPi.GPIO as GPIO
import time
import weather, max7219
from gpioenum import gpio
import wlogging
from wlogging import LogType, LogMessage
import tm1637l
from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

class ButtonStatus(Enum):
    OFF = 1
    SHORT_CLICK = 2
    LONG_CLICK = 3

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the pulse
PULSE_PIN = gpio.BUTTON_API_CHG.value

# Set up the GPIO pin as input
GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

# Function to detect click or double-click
def detect_button():
    click = 'none'
    if GPIO.input(PULSE_PIN) == 0:
        while GPIO.input(PULSE_PIN) == 0:
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  # Long click threshold (adjust as needed)
                # print('longClick')
                show_weather_api_name()
                return ButtonStatus.LONG_CLICK
            time.sleep(0.01)  # Adjust sleep time for responsiveness
        # print('shortClick')
        change_weather_api()
        return ButtonStatus.SHORT_CLICK
    # print('noClick')
    return ButtonStatus.OFF

# Change weather api
def change_weather_api():
    if weather.api_weather_id == 1:
        weather.api_weather_id = 2
        max7219.message='A2'
    elif weather.api_weather_id == 2:
        weather.api_weather_id = 3
        max7219.message='A3'
    elif weather.api_weather_id == 3:
        weather.api_weather_id = 4
        max7219.message='A4'
    else:
        weather.api_weather_id = 1
        max7219.message='A1'
    log = 'API' + str(weather.api_weather_id)
    wlogging.log(LogType.INFO.value,LogMessage.API_CHG.name,log)
    time.sleep(3)

# Show weather api name
def show_weather_api_name():
    api_name = 'API' + str(weather.api_weather_id) + ': ' + weather.api_weather_names[weather.api_weather_id-1]
    max7219.message=api_name
    wlogging.log(LogType.INFO.value,LogMessage.API_SHW.name,api_name)




