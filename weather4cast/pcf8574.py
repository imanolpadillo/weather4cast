# *************************************************************************************************** 
# ********************************************* PCF8574 *********************************************
# *************************************************************************************************** 
#    Source: 
#       https://pypi.org/project/pcf8574-io/
#    Prerequisites:
#       Enable I2C in raspi preferences
#       pip3 install smbus2
#       pip3 install pcf8574-io

import pcf8574_io
from weatherAPIenum import WeatherStatus

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

temperature_high = pcf8574_io.PCF(0x20)
temperature_low = pcf8574_io.PCF(0x21)
status = pcf8574_io.PCF(0x22)

# set pins as output
temperature_high.pin_mode("p0", "OUTPUT")
temperature_high.pin_mode("p1", "OUTPUT")
temperature_high.pin_mode("p2", "OUTPUT")
temperature_high.pin_mode("p3", "OUTPUT")
temperature_high.pin_mode("p4", "OUTPUT")
temperature_high.pin_mode("p5", "OUTPUT")
temperature_high.pin_mode("p6", "OUTPUT")
temperature_high.pin_mode("p7", "OUTPUT")
temperature_low.pin_mode("p0", "OUTPUT")
temperature_low.pin_mode("p1", "OUTPUT")
temperature_low.pin_mode("p2", "OUTPUT")
temperature_low.pin_mode("p3", "OUTPUT")
temperature_low.pin_mode("p4", "OUTPUT")
temperature_low.pin_mode("p5", "OUTPUT")
temperature_low.pin_mode("p6", "OUTPUT")
temperature_low.pin_mode("p7", "OUTPUT")
status.pin_mode("p0", "OUTPUT")
status.pin_mode("p1", "OUTPUT")
status.pin_mode("p2", "OUTPUT")
status.pin_mode("p3", "OUTPUT")
status.pin_mode("p4", "OUTPUT")
status.pin_mode("p5", "OUTPUT")
status.pin_mode("p6", "OUTPUT")
status.pin_mode("p7", "OUTPUT")

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def demo(flag):
    """
    Activates/deactivates all leds depending on flag value
    """
    global temperature_high
    global temperature_low
    global status
    if flag == True:
        value = "LOW"
    else:
        value = "HIGH"
    temperature_high.write("p0", value)
    temperature_high.write("p1", value)
    temperature_high.write("p2", value)
    temperature_high.write("p3", value)
    temperature_high.write("p4", value)
    temperature_high.write("p5", value)
    temperature_high.write("p6", value)
    temperature_high.write("p7", value)   # minus sign
    temperature_low.write("p0", value)
    temperature_low.write("p1", value)
    temperature_low.write("p2", value)
    temperature_low.write("p3", value)
    temperature_low.write("p4", value)
    temperature_low.write("p5", value)
    temperature_low.write("p6", value)
    temperature_low.write("p7", value)   # tomorrow rain led
    status.write("p0", value)  # sunny
    status.write("p1", value)  # partly cloudy
    status.write("p2", value)  # cloudy
    status.write("p3", value)  # rainy
    status.write("p4", value)  # foggy
    status.write("p5", value)  # stormy
    status.write("p6", value)  # snowy
    status.write("p7", value)  # windy
    


#   7-segment digit led position
#         p0
#      p5    p1
#         p6
#      p4    p2
#         p3       p7
def display_number(temperature_digit, value, disable_zero = False):
    """
    Activates leds for generating corresponding number
    """
    if value == 0:
        if disable_zero == False:
            temperature_digit.write("p0", "LOW")
            temperature_digit.write("p1", "LOW")
            temperature_digit.write("p2", "LOW")
            temperature_digit.write("p3", "LOW")
            temperature_digit.write("p4", "LOW")
            temperature_digit.write("p5", "LOW")
            temperature_digit.write("p6", "HIGH")
        else:
            temperature_digit.write("p0", "HIGH")
            temperature_digit.write("p1", "HIGH")
            temperature_digit.write("p2", "HIGH")
            temperature_digit.write("p3", "HIGH")
            temperature_digit.write("p4", "HIGH")
            temperature_digit.write("p5", "HIGH")
            temperature_digit.write("p6", "HIGH")
    elif value == 1:
        temperature_digit.write("p0", "HIGH")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "HIGH")
        temperature_digit.write("p4", "HIGH")
        temperature_digit.write("p5", "HIGH")
        temperature_digit.write("p6", "HIGH")
    elif value == 2:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "HIGH")
        temperature_digit.write("p3", "LOW")
        temperature_digit.write("p4", "LOW")
        temperature_digit.write("p5", "HIGH")
        temperature_digit.write("p6", "LOW")
    elif value == 3:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "LOW")
        temperature_digit.write("p4", "HIGH")
        temperature_digit.write("p5", "HIGH")
        temperature_digit.write("p6", "LOW")
    elif value == 4:
        temperature_digit.write("p0", "HIGH")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "HIGH")
        temperature_digit.write("p4", "HIGH")
        temperature_digit.write("p5", "LOW")
        temperature_digit.write("p6", "LOW")
    elif value == 5:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "HIGH")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "LOW")
        temperature_digit.write("p4", "HIGH")
        temperature_digit.write("p5", "LOW")
        temperature_digit.write("p6", "LOW")
    elif value == 6:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "HIGH")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "LOW")
        temperature_digit.write("p4", "LOW")
        temperature_digit.write("p5", "LOW")
        temperature_digit.write("p6", "LOW")
    elif value == 7:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "HIGH")
        temperature_digit.write("p4", "HIGH")
        temperature_digit.write("p5", "HIGH")
        temperature_digit.write("p6", "HIGH")
    elif value == 8:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "LOW")
        temperature_digit.write("p4", "LOW")
        temperature_digit.write("p5", "LOW")
        temperature_digit.write("p6", "LOW")
    elif value == 9:
        temperature_digit.write("p0", "LOW")
        temperature_digit.write("p1", "LOW")
        temperature_digit.write("p2", "LOW")
        temperature_digit.write("p3", "LOW")
        temperature_digit.write("p4", "HIGH")
        temperature_digit.write("p5", "LOW")
        temperature_digit.write("p6", "LOW")

def display_temperature (value):
    """
    Displays temperature
    """
    global temperature_high
    global temperature_low
    # Extract tens and units digits
    tens = value // 10
    units = value % 10
    display_number(temperature_high, tens, True)
    display_number(temperature_low, units)
    # Display sign
    if value < 0:
        temperature_high.write("p7", "LOW")
    else:
        temperature_high.write("p7", "HIGH")

def display_status(value):
    """
    Displays weather status led
    """
    global status
    status.write("p0", "HIGH")
    status.write("p1", "HIGH")
    status.write("p2", "HIGH")
    status.write("p3", "HIGH")
    status.write("p4", "HIGH")
    status.write("p5", "HIGH")
    status.write("p6", "HIGH")
    status.write("p7", "HIGH")
    if value == WeatherStatus.SUNNY:
        status.write("p0", "LOW")
    elif value == WeatherStatus.PARTLY_CLOUDY:
        status.write("p1", "LOW")
    elif value == WeatherStatus.CLOUDY:
        status.write("p2", "LOW")
    elif value == WeatherStatus.RAINY:
        status.write("p3", "LOW")
    elif value == WeatherStatus.FOGGY:
        status.write("p4", "LOW")
    elif value == WeatherStatus.STORMY:
        status.write("p5", "LOW")
    elif value == WeatherStatus.SNOWY:
        status.write("p6", "LOW")
    elif value == WeatherStatus.WINDY:
        status.write("p7", "LOW")

def toggle_rain():
    """
    Toogle rain status
    """
    rain_pin="p3"
    if status.read(rain_pin) == True:
        status.write(rain_pin, "LOW")
    else:
        status.write(rain_pin, "HIGH")

def tomorrow_rain(flag):
    """
    tomorrow_rain_pin is activated or not depending on flag value
    """
    tomorrow_rain_pin="p7"
    if flag == True:
        temperature_low.write(tomorrow_rain_pin, "LOW")
    else:
        temperature_low.write(tomorrow_rain_pin, "HIGH")
