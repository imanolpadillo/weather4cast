# *************************************************************************************************** 
# ********************************************* MAX7219 *********************************************
# *************************************************************************************************** 
#   Source:
#       https://luma-led-matrix.readthedocs.io/en/latest/install.html#pre-requisites
#   Prerequisites:
#       sudo usermod -a -G spi,gpio pi
#       sudo apt install build-essential python3-dev python3-pip libfreetype6-dev libjpeg-dev libopenjp2-7 libtiff5
#       sudo -H pip install --upgrade --ignore-installed pip setuptools
#       sudo python3 -m pip install --upgrade luma.led_matrix
#       (optional) https://github.com/rm-hull/luma.led_matrix.git
#       (optional) python3 ./luma.led_matrix/examples/matrix_demo.py --cascade=2 --block-orientation=-90

from weatherAPIenum import WeatherConfig
from PIL import Image
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
timeout = 2
level =  [0] * 16
message = ""

# create matrix device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=2, block_orientation=-90,
                    rotate=0, blocks_arranged_in_reverse_order=False)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
def demo(flag):
    """
    Activates/deactivates all leds depending on flag value
    """
    if flag == True:
        show_level([8] * 16)  # all leds activated
    else:
        show_level([0] * 16)  # all leds deactivated
    
def show_message(message = message):
    """
    shows string message
    :param message: string to show
    :return: -
    """
    # Display message
    with canvas(device) as draw:
        text(draw, (0, 0), message, fill="white")


def show_level(level = level):
    """
    shows level
    :param level: 16 array including precipitation probability
    :return: -
    """
    # Display the level
    level_array = []
    for row in reversed(range(8)):
        limit = row * WeatherConfig.RAIN_STEP.value + WeatherConfig.RAIN_STEP.value  #row_7 -> 4, row_6 -> 3.5 ... row_0 -> 0.5
        for rain_hour in level:
            if rain_hour >= limit:
                level_array.append(1)
            else:
                level_array.append(0)
    image = Image.new("1", (16, 8))
    image.putdata(level_array)
    device.display(image)
