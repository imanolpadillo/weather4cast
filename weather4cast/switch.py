# *************************************************************************************************** 
# ********************************************** SWITCH *********************************************
# *************************************************************************************************** 
import RPi.GPIO as GPIO
from gpioenum import gpio
# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
GPIO.setmode(GPIO.BCM)
DAY_PIN = gpio.SWITCH_DAY.value
HOUR_PIN = gpio.SWITCH_HOUR.value
forecast_day_flag = False
forecast_hour_flag = False

# Set up the GPIO pin as input with pull-down resistor
GPIO.setup(DAY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HOUR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def switch_state(PIN):
    """
    Function to detect the state of the switch.
    Returns True if the switch is pressed, False otherwise.
    """
    return GPIO.input(PIN) == GPIO.HIGH

def update():
    """
    updates switch current value.
    """
    global forecast_day_flag, forecast_hour_flag
    forecast_day_flag = switch_state(DAY_PIN)
    forecast_hour_flag = switch_state(HOUR_PIN)
