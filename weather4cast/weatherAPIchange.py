# *************************************************************************************************** 
# ***************************************** WeatherAPIchange ****************************************
# *************************************************************************************************** 
import RPi.GPIO as GPIO
import time
from gpioenum import gpio
from weatherAPIenum import WeatherButton

# When a standalone press lasts at least one second, watch for SuperLongClick.
super_long_click_flag = False
# A completed superlong gesture must not reuse the still-held press.
ignore_until_release = False

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
    """Detect up to 24 short taps, optionally followed by a held tap.

    Short-tap sequences finish after a 0.5s release gap. A following hold
    lasts 1s for numbered LongClick (reported on release), or 3s for
    numbered SuperLongClick (reported while held). Hold time excludes gaps.
    Standalone holds retain LongClick at 1s, then SuperLongClick after a
    further 2s in the next call if the button remains pressed.
    """
    global super_long_click_flag
    global ignore_until_release

    if ignore_until_release:
        if GPIO.input(PULSE_PIN) == 1:
            return WeatherButton.NoClick
        ignore_until_release = False

    if GPIO.input(PULSE_PIN) == 1:
        if not super_long_click_flag:
            return WeatherButton.NoClick
        start_time = time.monotonic()
        while GPIO.input(PULSE_PIN) == 1:
            if time.monotonic() - start_time >= 2.0:
                super_long_click_flag = False
                ignore_until_release = True
                return WeatherButton.SuperLongClick
            time.sleep(0.01)
        super_long_click_flag = False
        return WeatherButton.NoClick

    super_long_click_flag = False
    while GPIO.input(PULSE_PIN) == 0:
        time.sleep(0.01)

    short_clicks = 0
    while True:
        press_started = time.monotonic()
        while GPIO.input(PULSE_PIN) == 1:
            held_for = time.monotonic() - press_started
            if short_clicks == 0 and held_for >= 1.0:
                super_long_click_flag = True
                return WeatherButton.LongClick
            if short_clicks > 0 and held_for >= 3.0:
                ignore_until_release = True
                return WeatherButton(300 + short_clicks)
            time.sleep(0.01)

        released_at = time.monotonic()
        held_for = released_at - press_started
        if short_clicks > 0:
            if held_for >= 3.0:
                return WeatherButton(300 + short_clicks)
            if held_for >= 1.0:
                return WeatherButton(100 + short_clicks)
        elif held_for >= 1.0:
            return WeatherButton.LongClick

        # Saturate at the highest supported count, but still allow its hold.
        short_clicks = min(short_clicks + 1, 24)
        while GPIO.input(PULSE_PIN) == 0:
            if time.monotonic() - released_at >= 0.5:
                return WeatherButton(short_clicks)
            time.sleep(0.01)


