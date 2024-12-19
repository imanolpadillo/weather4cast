# *************************************************************************************************** 
# *********************************************** KY040 *********************************************
# *************************************************************************************************** 
# A) KY-040
#    Source: 
#       https://github.com/AllanGallop/RPi_GPIO_Rotary/tree/master
#   Prerequisites:
#       pip3 install RPi-GPIO-Rotary
import max7219
import time
from RPi_GPIO_Rotary import rotary
from gpioenum import gpio

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
forecast_day = 1   # 0=today, 1=tomorrow...
forecast_hour = 0  # 0=00:00, 1=01:00 ... 23=23:00

HourDialCLK = gpio.KY040_HOUR_CLK.value
HourDialDT = gpio.KY040_HOUR_DT.value
HourDialSW = gpio.KY040_HOUR_SW.value

DayDialCLK = gpio.KY040_DAY_CLK.value
DayDialDT = gpio.KY040_DAY_DT.value
DayDialSW = gpio.KY040_DAY_SW.value

prev_counter = 0
counter = 0
lastWasInc = False

CLICK_MS = 1000   # 2 clicks in less than CLICK_MS means a doble click
dayDial_last_pushed_ms = 0
dayDial_One_click = False
hourDial_last_pushed_ms = 0
hourDial_One_click = False

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

## Define DAY-Callback functions
def dayDialTurnInc():
    """
    Incremental change detected
    """
    print("") #+day

def dayDialTurnDec():
    """
    Decremental change detected
    """
    print("") #-day

def dayDialPushed():
    """
    Push button activated
    """
    global CLICK_MS
    global dayDial_last_pushed_ms
    global dayDial_One_click
    if abs(int(time.time() * 1000) - dayDial_last_pushed_ms) < CLICK_MS:
        day_dial.stop()
        day_dial.start()
        setForecastDay(1)
        dayDial_One_click = False
        #print("reset day")
    else:
        dayDial_One_click = True
    dayDial_last_pushed_ms = int(time.time() * 1000)

def dayDialChanged(count):
    # print(count) ## Current Counter value
    setForecastDay(count)

# 00=day1, 04=day2, 08=day3, 12=day4, 16=day5
def setForecastDay(count):
    global forecast_day
    while count<0:
        count += 20
    while count>=20:
        count -= 20
    if count>=0 and count<4:
        forecast_day = 1
    elif count>=4 and count<8:
        forecast_day = 2
    elif count>=8 and count<12:
        forecast_day = 3
    elif count>=12 and count<16:
        forecast_day = 4
    elif count>=16:
        forecast_day = 5
    max7219.message = str(forecast_day)

## Define HOUR-Callback functions
def hourDialTurnInc():
    global lastWasInc
    lastWasInc = True
    # print("+ hour")

def hourDialTurnDec():
    global lastWasInc
    lastWasInc = False
    # print("- hour")

def hourDialPushed():
    global CLICK_MS
    global hourDial_last_pushed_ms
    global hourDial_One_click
    if abs(int(time.time() * 1000) - hourDial_last_pushed_ms) < CLICK_MS:
        hour_dial.stop()
        hour_dial.start()
        setForecastHour(0)
        hourDial_One_click = False
        # print("reset hour")
    else:
        hourDial_One_click = True
    hourDial_last_pushed_ms = int(time.time() * 1000)

def hourDialChanged(count):
    # print(count) ## Current Counter value
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
            forecast_hour = 0

    if len(str(forecast_hour))==1:
        max7219.message = '0' + str(forecast_hour)
    else:
        max7219.message = str(forecast_hour)


## DAY START
## Initialise (DayDialCLK, DayDialDT, DayDialSW, ticks)
day_dial = rotary.Rotary(DayDialCLK,DayDialDT,DayDialSW,2)

 ## Register callbacks
day_dial.register(increment=dayDialTurnInc, decrement=dayDialTurnDec)

## Register more callbacks
day_dial.register(pressed=dayDialPushed, onchange=dayDialChanged) 

## Start monitoring the encoder
day_dial.start() 

## HOUR START
## Initialise (HourDialCLK, HourDialDT, HourDialSW, ticks)
hour_dial = rotary.Rotary(HourDialCLK,HourDialDT,HourDialSW,2)

 ## Register callbacks
hour_dial.register(increment=hourDialTurnInc, decrement=hourDialTurnDec)

## Register more callbacks
hour_dial.register(pressed=hourDialPushed, onchange=hourDialChanged) 

## Start monitoring the encoder
hour_dial.start() 



# ## Stop monitoring
# hour_dial.stop()
