# *************************************************************************************************** 
# ********************************************** TM1637 *********************************************
# *************************************************************************************************** 
#   Source:
#       https://github.com/depklyon/raspberrypi-tm1637
#   Prerequisites:
#       pip3 install raspberrypi-tm1637    

import tm1637
import weather
from datetime import datetime
import pytz
from gpioenum import gpio
from weatherAPIenum import WeatherConfig

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
tmin = tm1637.TM1637(clk=gpio.TM1637_TMIN_CLK.value, dio=gpio.TM1637_TMIN_DIO.value)
tmax = tm1637.TM1637(clk=gpio.TM1637_TMAX_CLK.value, dio=gpio.TM1637_TMAX_DIO.value)
tmin.brightness(WeatherConfig.INTENSITY_7LED_MODE_0N.value)
tmax.brightness(WeatherConfig.INTENSITY_7LED_MODE_0N.value)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
def demo(flag, led_intensity = WeatherConfig.INTENSITY_7LED_MODE_0N.value):
    """
    Activates/deactivates all leds depending on flag value
    """
    tmax.brightness(led_intensity)
    tmin.brightness(led_intensity)
    if flag == True:
        # all LEDS on "88:88"
        tmin.write([127, 255, 127, 127])
        tmax.write([127, 255, 127, 127])
    else:
        # all LEDS off
        tmin.write([0, 0, 0, 0])
        tmax.write([0, 0, 0, 0])

def show_api_error(led_intensity = WeatherConfig.INTENSITY_7LED_MODE_0N.value):
    """
    displays 'api err' in 7-segment displays.
    """
    tmax.brightness(led_intensity)
    tmin.brightness(led_intensity)
    tmax.show(' api')
    tmin.show(' err')

def show_api_name(led_intensity = WeatherConfig.INTENSITY_7LED_MODE_0N.value):
    """
    displays current weather api name in 7-segment displays.
    """
    tmax.brightness(led_intensity)
    tmin.brightness(led_intensity)
    api_name = weather.get_current_weather_api_name()
    tmax.show(api_name[:4])   # first 4 characters
    tmin.show(api_name[4:8])  # next 4 characters
        
def show_temperature(min, max, led_intensity = WeatherConfig.INTENSITY_7LED_MODE_0N.value):
    """
    shows min and max temperature
    :param min: min temperature
    :param max: max temperature
    """
    tmax.brightness(led_intensity)
    tmin.brightness(led_intensity)
    tmin.temperature(int(min))
    tmax.temperature(int(max))

def show_date_time(led_intensity = WeatherConfig.INTENSITY_7LED_MODE_0N.value, time_and_date = False):
    """
    shows date and time
    """ 
    # Get the current date and time
    now = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))
    tmax.brightness(led_intensity)
    tmin.brightness(led_intensity)

    if time_and_date:
        tmax.numbers(now.day, now.month, colon=False)
        tmin.numbers(now.hour, now.minute)
    else:
        tmax.numbers(now.hour, now.minute)
        tmin.write([0, 0, 0, 0])
