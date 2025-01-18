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
    '''
    __   SuperLongClick 
    _    LongClick
    ._   ShortLongClick
    ..-  ShortShortLongClick
    .    ShortClick
    ..   DoubleClick
    ...  TripleClick
    '''
    global super_long_click_flag
    if GPIO.input(PULSE_PIN) == 0:
        super_long_click_flag = False
        while GPIO.input(PULSE_PIN) == 0:
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('longClick')
                super_long_click_flag = True
                return WeatherButton.LongClick            # LongClick threshold 
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('shortClick')
                return WeatherButton.x01Click             # x01Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('shortLongClick')
                return WeatherButton.ShortLongClick       # ShortLongClick threshold 
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('doubleClick')
                return WeatherButton.x02Click             # x02Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('shortShortLongClick')
                return WeatherButton.ShortShortLongClick  # ShortShortLongClick threshold 
            time.sleep(0.01) 
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('trippleClick')
                return WeatherButton.x03Click             # x03Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('cuadrupleClick')
                return WeatherButton.x04Click             # x04Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('quintupleClick')
                return WeatherButton.x05Click             # x05Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('sextupleClick')
                return WeatherButton.x06Click             # x06Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x07Click             # x07Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x08Click             # x08Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x09Click             # x09Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x10Click             # x10Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x11Click             # x11Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x12Click             # x12Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x13Click             # x13Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x14Click             # x14Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x15Click             # x15Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x16Click             # x16Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x17Click             # x17Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x18Click             # x18Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x19Click             # x19Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x20Click             # x20Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x21Click             # x21Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x22Click             # x22Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x23Click             # x23Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 0:
            if time.time() - start_time >= 0.5:  
                # print('xClick')
                return WeatherButton.x24Click             # x24Click threshold 
            time.sleep(0.01) 
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 1.0:  
                # print('noClick')
                return WeatherButton.NoClick              # NoClick threshold
            time.sleep(0.01)

    elif super_long_click_flag == True:
        # long click remains
        start_time = time.time()
        while GPIO.input(PULSE_PIN) == 1:
            if time.time() - start_time >= 2.0:  
                super_long_click_flag = False
                # print('superLongClick')
                return WeatherButton.SuperLongClick       # SuperLongClick threshold 
        super_long_click_flag = False
        return WeatherButton.NoClick                 
    # print('noClick')
    return WeatherButton.NoClick






