# *************************************************************************************************** 
# ********************************************** TM1637 *********************************************
# *************************************************************************************************** 
#   Source:
#       https://github.com/depklyon/raspberrypi-tm1637
#   Prerequisites:
#       pip3 install raspberrypi-tm1637    

import tm1637
from gpioenum import gpio

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
tmin = tm1637.TM1637(clk=gpio.TM1637_TMIN_CLK.value, dio=gpio.TM1637_TMIN_DIO.value)
tmax = tm1637.TM1637(clk=gpio.TM1637_TMAX_CLK.value, dio=gpio.TM1637_TMAX_DIO.value)

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


def show_temperature(min, max):
    """
    shows min and max temperature
    :param min: min temperature
    :param max: max temperature
    :return: -
    """
    tmin.temperature(int(min))
    tmax.temperature(int(max))
