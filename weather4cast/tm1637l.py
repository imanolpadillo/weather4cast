# *************************************************************************************************** 
# ********************************************** TM1637 *********************************************
# *************************************************************************************************** 
#   Source:
#       https://github.com/depklyon/raspberrypi-tm1637
#   Prerequisites:
#       pip3 install raspberrypi-tm1637    

import tm1637
import weather
from gpioenum import gpio
from weatherAPIenum import WeatherConfig

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
tmin = tm1637.TM1637(clk=gpio.TM1637_TMIN_CLK.value, dio=gpio.TM1637_TMIN_DIO.value)
tmax = tm1637.TM1637(clk=gpio.TM1637_TMAX_CLK.value, dio=gpio.TM1637_TMAX_DIO.value)
tmin.brightness(WeatherConfig.INTENSITY_7LED.value)
tmax.brightness(WeatherConfig.INTENSITY_7LED.value)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
def demo(flag):
    """
    Activates/deactivates all leds depending on flag value
    """
    if flag == True:
        # all LEDS on "88:88"
        tmin.write([127, 255, 127, 127])
        tmax.write([127, 255, 127, 127])
    else:
        # all LEDS off
        tmin.write([0, 0, 0, 0])
        tmax.write([0, 0, 0, 0])

def show_api_error():
    """
    displays 'api err' in 7-segment displays.
    """
    tmax.show(' api')
    tmin.show(' err')

def show_api_name():
    """
    displays current weather api name in 7-segment displays.
    """
    api_name = weather.get_current_weather_api_name()
    tmax.show(api_name[:4])   # first 4 characters
    tmin.show(api_name[4:8])  # next 4 characters
        
def show_temperature(min, max):
    """
    shows min and max temperature
    :param min: min temperature
    :param max: max temperature
    """
    tmin.temperature(int(min))
    tmax.temperature(int(max))
