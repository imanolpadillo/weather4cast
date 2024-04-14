# *************************************************************************************************** 
# *********************************************** KY040 *********************************************
# *************************************************************************************************** 
# A) KY-040
#    Source: 
#       https://github.com/AllanGallop/RPi_GPIO_Rotary/tree/master
#   Prerequisites:
#       pip3 install RPi-GPIO-Rotary
import time
from RPi_GPIO_Rotary import rotary

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
forecast_day = 0   # 0=today, 1=tomorrow...
forecast_hour = 0  # 0=00:00, 1=01:00 ... 23=23:00

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

CLK = 24
DT = 17
SW = 27

## Define Callback functions
def cwTurn():
    print("CW Turn")

def ccwTurn():
    print("CCW Turn")

def buttonPushed():
    print("Button Pushed")

def valueChanged(count):
    print(count) ## Current Counter value

## Initialise (clk, dt, sw, ticks)
obj = rotary.Rotary(CLK,DT,SW,2)

 ## Register callbacks
obj.register(increment=cwTurn, decrement=ccwTurn)

## Register more callbacks
obj.register(pressed=buttonPushed, onchange=valueChanged) 

## Start monitoring the encoder
obj.start() 

while True:
    time.sleep(0.5)

## Stop monitoring
obj.stop()