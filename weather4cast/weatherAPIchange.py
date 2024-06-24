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
ultra_long_click_flag = False

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
    '''
    _____ Ultra long click
    ___   Super long click
    __    Long click
    _ __  Short click + long click
    _     Short click
    _ _   Double click
    _ _ _ Triple click
    '''
    global super_long_click_flag
    global ultra_long_click_flag
    if GPIO.input(PULSE_PIN) == 0:
        super_long_click_flag = False
        while GPIO.input(PULSE_PIN) == 0:
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('longClick')
                super_long_click_flag = True
                return WeatherButton.LongClick       # Long click threshold 
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('shortClick')
                return WeatherButton.ShortClick      # Short click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('shortLongClick')
                return WeatherButton.ShortLongClick  # Short click + long click threshold 
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('doubleClick')
                return WeatherButton.DoubleClick     # Double click threshold 
            time.sleep(0.01) 
        # print('trippleClick')
        return WeatherButton.TrippleClick            # Tripple click threshold 
    elif super_long_click_flag == True:
        # long click remains
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 2.0:  
                super_long_click_flag = False
                ultra_long_click_flag = True
                # print('superLongClick')
                return WeatherButton.SuperLongClick  # Super long click threshold 
        super_long_click_flag = False
        ultra_long_click_flag = True 
        return WeatherButton.NoClick
    elif ultra_long_click_flag == True:
        # long click remains
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 2.0:  
                # print('ultraLongClick')
                ultra_long_click_flag = False
                return WeatherButton.UltraLongClick  # Ultra long click threshold  
        ultra_long_click_flag = False
        return WeatherButton.NoClick                   
    # print('noClick')
    return WeatherButton.NoClick






