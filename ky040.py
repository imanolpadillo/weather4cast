# *************************************************************************************************** 
# *********************************************** KY040 *********************************************
# *************************************************************************************************** 
# A) KY-040
#    Source: 
#       https://github.com/AllanGallop/RPi_GPIO_Rotary/tree/master
#   Prerequisites:
#       pip3 install RPi-GPIO-Rotary
import max7219
from RPi_GPIO_Rotary import rotary

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
forecast_day = 0   # 0=today, 1=tomorrow...
forecast_hour = 0  # 0=00:00, 1=01:00 ... 23=23:00

HourDialCLK = 24
HourDialDT = 17
HourDialSW = 27

prev_counter = 0
counter = 0
lastWasInc = False

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

## Define Callback functions
def hourDialTurnInc():
    global lastWasInc
    lastWasInc = True
    # print("CW Turn")

def hourDialTurnDec():
    global lastWasInc
    lastWasInc = False
    # print("CCW Turn")

def hourDialPushed():
    hour_dial.stop()
    hour_dial.start()
    setForecastHour(0)
    # print("Button Pushed")

def hourDialChanged(count):
    print(count) ## Current Counter value
    setForecastHour(count)

def setForecastHour(count):
    global lastWasInc
    global forecast_hour
    while count<0:
        count += 20
    while count>20:
        count -= 20
    if lastWasInc == True:
        if count == 0:
            forecast_hour = 0
        elif count == 1:
            forecast_hour = 1
        elif count == 2:
            forecast_hour = 2
        elif count == 3:
            forecast_hour = 3
        elif count == 4:
            forecast_hour = 4
        elif count == 5:
            forecast_hour = 6
        elif count == 6:
            forecast_hour = 7
        elif count == 7:
            forecast_hour = 8
        elif count == 8:
            forecast_hour = 9
        elif count == 9:
            forecast_hour = 10
        elif count == 10:
            forecast_hour = 12
        elif count == 11:
            forecast_hour = 13
        elif count == 12:
            forecast_hour = 14
        elif count == 13:
            forecast_hour = 15
        elif count == 14:
            forecast_hour = 16
        elif count == 15:
            forecast_hour = 18
        elif count == 16:
            forecast_hour = 19
        elif count == 17:
            forecast_hour = 20
        elif count == 18:
            forecast_hour = 21
        elif count == 19:
            forecast_hour = 22
        elif count == 20:
            forecast_hour = 00
    else:
        if count == 0:
            forecast_hour = 0
        elif count == 1:
            forecast_hour = 2
        elif count == 2:
            forecast_hour = 3
        elif count == 3:
            forecast_hour = 4
        elif count == 4:
            forecast_hour = 5
        elif count == 5:
            forecast_hour = 6
        elif count == 6:
            forecast_hour = 8
        elif count == 7:
            forecast_hour = 9
        elif count == 8:
            forecast_hour = 10
        elif count == 9:
            forecast_hour = 11
        elif count == 10:
            forecast_hour = 12
        elif count == 11:
            forecast_hour = 14
        elif count == 12:
            forecast_hour = 15
        elif count == 13:
            forecast_hour = 16
        elif count == 14:
            forecast_hour = 17
        elif count == 15:
            forecast_hour = 18
        elif count == 16:
            forecast_hour = 20
        elif count == 17:
            forecast_hour = 21
        elif count == 18:
            forecast_hour = 22
        elif count == 19:
            forecast_hour = 23
        elif count == 20:
            forecast_hour = 00
    max7219.message = str(forecast_hour)


## Initialise (HourDialCLK, HourDialDT, HourDialSW, ticks)
hour_dial = rotary.Rotary(HourDialCLK,HourDialDT,HourDialSW,2)

 ## Register callbacks
hour_dial.register(increment=hourDialTurnInc, decrement=hourDialTurnDec)

## Register more callbacks
hour_dial.register(pressed=hourDialPushed, onchange=hourDialChanged) 

## Start monitoring the encoder
hour_dial.start() 

# while True:
#     time.sleep(0.5)

# ## Stop monitoring
# hour_dial.stop()