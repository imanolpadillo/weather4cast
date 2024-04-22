import RPi.GPIO as GPIO
import threading
import time
import weather, max7219


# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the pulse
PULSE_PIN = 13

# Set up the GPIO pin as input
GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Function to handle pulse detection
def pulse_detector():
    if GPIO.input(PULSE_PIN):
        if weather.api_weather_id == 1:
            weather.api_weather_id = 2
            max7219.message='A2'
            print("Change to weatherAPI2")
        else:
            weather.api_weather_id = 1
            max7219.message='A1'
            print("Change to weatherAPI1")
        time.sleep(3)
        return True
    else:
        return False



