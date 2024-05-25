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

from weatherAPIenum import WeatherConfig, WeatherRainStep, WeatherTimeLine
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
    global level
    if flag == True:
        level = [1] * 16 * 8
        show_level()  # all leds activated
    else:
        level = [0] * 16 * 8
        show_level()  # all leds deactivated

def round_to_step(input_values, step = WeatherConfig.RAIN_STEP.value):
    """
    Rounds each value in input_values to the nearest multiple of the step.
   
    Args:
    - step (float): The step size to round to.
    - input_values (list of floats): The list of input values to round.
   
    Returns:
    - list of floats: The rounded values.
    """
    rounded_values = [round(value / step) * step for value in input_values]
    return rounded_values

    
def show_message(message = message):
    """
    shows string message
    :param message: string to show
    :return: -
    """
    # Display message
    with canvas(device) as draw:
        text(draw, (0, 0), message, fill="white")


def calculate_level(input_level, weather_timeline = WeatherTimeLine.T16):
    """
    shows level
    :param level: 16 array including precipitation probability
    :return: -
    """
    global level
    # Get max value of array and adjust rain_step, activated_led, deactivated_led
    activated_led = 1
    deactivated_led = 0
    rain_step = WeatherConfig.RAIN_STEP.value
    if WeatherConfig.RAIN_STEP_MODE.value == WeatherRainStep.AUTO.value:
        max_level = max(input_level)
        if max_level > 8 * rain_step:
            rain_step = rain_step * 2 
            activated_led = 0
            deactivated_led = 1

    # Round values
    input_level = round_to_step(input_level, rain_step)

    # Display the level
    output_level = []
    for row in reversed(range(8)):
        limit = row * rain_step + rain_step  #row_7 -> 4, row_6 -> 3.5 ... row_0 -> 0.5
        for rain_hour in input_level:
            if rain_hour >= limit:
                output_level.append(activated_led)
            else:
                output_level.append(deactivated_led)

    # Set T24, T48 markers
    if weather_timeline == WeatherTimeLine.T24:
        # Toggle the value at position 15
        output_level[15] ^= 1  # XOR operation to toggle between 0 and 1
    elif weather_timeline == WeatherTimeLine.T48:
        # Toggle the value at position 15
        output_level[15] ^= 1  # XOR operation to toggle between 0 and 1
        output_level[14] ^= 1  # XOR operation to toggle between 0 and 1
    elif weather_timeline == WeatherTimeLine.T120:
        # Toggle the value at position 15
        output_level[0] ^= 1  # XOR operation to toggle between 0 and 1
        output_level[3] ^= 1  # XOR operation to toggle between 0 and 1
        output_level[6] ^= 1  # XOR operation to toggle between 0 and 1
        output_level[9] ^= 1  # XOR operation to toggle between 0 and 1
        output_level[12] ^= 1  # XOR operation to toggle between 0 and 1
    level = output_level



def show_level():
    global level
    image = Image.new("1", (16, 8))
    image.putdata(level)
    device.display(image)