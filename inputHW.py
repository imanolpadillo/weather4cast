# *************************************************************************************************** 
# ********************************************* INPUT HW ********************************************
# *************************************************************************************************** 
# A) ADS1115
#    Source: 
#       https://www.engineersgarage.com/raspberry-pi-ads1015-ads1115-analog-sensor-interfacing-ir-sensor-interfacing/
#    Prerequisites:
#       Enable I2C in raspi preferences
#       sudo apt-get update
#       sudo apt-get install build-essential python-dev-is-python2 python3-smbus python3-pip
#       sudo pip3 install adafruit_ads1x15

import Adafruit_ADS1x15
GAIN = 1

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
forecast_day = 0   # 0=today, 1=tomorrow...
forecast_hour = 0  # 0=00:00, 1=01:00 ... 23=23:00

adc = Adafruit_ADS1x15.ADS1115()

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

value = adc.read_adc(0, gain=GAIN)
analog_voltage = value*(4.096/32767)
