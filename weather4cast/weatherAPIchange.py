# *************************************************************************************************** 
# ***************************************** WeatherAPIchange ****************************************
# *************************************************************************************************** 
import RPi.GPIO as GPIO
import time
import weather, max7219
from gpioenum import gpio
import wlogging
from wlogging import LogType, LogMessage
from enum import Enum
from weatherAPIenum import WeatherTimeLine, WeatherButton

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
# When button is pressed>1second, this flag is activated.
super_long_click_flag = False

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the pulse
PULSE_PIN = gpio.BUTTON_API_CHG.value

# Set up the GPIO pin as input
GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

# Function to detect click
def detect_button():
    global super_long_click_flag
    click = 'none'
    if GPIO.input(PULSE_PIN) == 0:
        super_long_click_flag = False
        while GPIO.input(PULSE_PIN) == 0:
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  # Long click threshold 
                # print('longClick')
                super_long_click_flag = True
                return WeatherButton.LongClick
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  # Short click threshold 
                # print('shortClick')
                return WeatherButton.ShortClick   
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  # Short click threshold 
                # print('doubleClick')
                return WeatherButton.DoubleClick   
            time.sleep(0.01) 
        # print('trippleClick')
        return WeatherButton.TrippleClick
    elif super_long_click_flag == True:
        # long click remains
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 2.0:  # Super long click threshold 
                # print('superLongClick')
                super_long_click_flag = False
                return WeatherButton.SuperLongClick        
    # print('noClick')
    return WeatherButton.NoClick






