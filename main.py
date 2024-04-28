# *************************************************************************************************** 
# ************************************************ MAIN *********************************************
# *************************************************************************************************** 
import weather, weatherAPIchange
import max7219
import tm1637l
import ky040
import pcf8574
import switch
from time import strftime
import threading, time
import pytz
from datetime import datetime

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
WEATHER_API_REFRESH_TIME = 1800 # in seconds
weather_refresh_flag = False
thread_max7219_running = True

class ForecastInput:
    def __init__(self, dayFlag=False, hourFlag=False, day=0, hour=0):
        self.dayFlag = dayFlag
        self.hourFlag = hourFlag
        self.day = day
        self.hour = hour
forecast_input = ForecastInput()
prev_forecast_input = ForecastInput()

# *************************************************************************************************** 
# THREADS
# *************************************************************************************************** 
def thread_weatherAPI(f_stop):
    madrid_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(madrid_tz)
    print('call weatherAPI' + str(weather.api_weather_id) + ': ' + now.strftime("%H:%M:%S"))
    weather.refresh()
    global weather_refresh_flag
    weather_refresh_flag = True
    if not f_stop.is_set():
        threading.Timer(WEATHER_API_REFRESH_TIME, thread_weatherAPI, [f_stop]).start()

def thread_max7219_function():
    global thread_max7219_running
    while (thread_max7219_running):
        if max7219.message != "":
            max7219.show_message(max7219.message)
            max7219.message = ""
        else:
            max7219.show_level(max7219.level)
        time.sleep(max7219.timeout)

# Function to handle pulse detection
def thread_changeAPI_function():
    global weather_refresh_flag
    while True:
        if weatherAPIchange.pulse_detector():
            weather_refresh_flag = True
        time.sleep(0.01)  # Adjust as needed for your application

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def input_data_refresh():
    change_flag = False
    global weather_refresh_flag
    switch.update()
    forecast_input.dayFlag = switch.forecast_day_flag
    forecast_input.hourFlag = switch.forecast_hour_flag
    if forecast_input.dayFlag == False:
        forecast_input.day = 0
    else:
        forecast_input.day = ky040.forecast_day
    if forecast_input.hourFlag == False:
        # Get the timezone for Madrid
        madrid_tz = pytz.timezone('Europe/Madrid')
        now = datetime.now(madrid_tz)
        forecast_input.hour = now.strftime("%H")
    else:
        forecast_input.hour = ky040.forecast_hour

    if forecast_input.dayFlag != prev_forecast_input.dayFlag:
        change_flag = True
    if forecast_input.hourFlag != prev_forecast_input.hourFlag:
        change_flag = True
    if forecast_input.hour != prev_forecast_input.hour:
        change_flag = True
    if forecast_input.dayFlag == True and (forecast_input.day != prev_forecast_input.day):
        change_flag = True

    if change_flag == True:
        print("INPUT_DATA: day_flag=" + str(forecast_input.dayFlag) + ", hour_flag=" + str(forecast_input.hourFlag) + \
              ", day=" + str(forecast_input.day) + ", hour=" + str(forecast_input.hour))
        weather_refresh_flag = True

    prev_forecast_input.dayFlag = forecast_input.dayFlag
    prev_forecast_input.hourFlag = forecast_input.hourFlag
    prev_forecast_input.day = forecast_input.day
    prev_forecast_input.hour = forecast_input.hour


# *************************************************************************************************** 
# main
# *************************************************************************************************** 

# start threads
f_stop = threading.Event()
thread_weatherAPI(f_stop)

thread_max7219 = threading.Thread(target=thread_max7219_function)
thread_max7219.start()

thread_changeAPI = threading.Thread(target=thread_changeAPI_function)
thread_changeAPI.start()

# infinite loop
while True:
    input_data_refresh()
    if weather_refresh_flag == True:
        try:
            weather_refresh_flag = False
            # display min/max temperature
            [tmin,tmax]=weather.get_min_max_temperature(forecast_input.day)
            tm1637l.show_temperature(tmin,tmax)
            print('tmin=' + str(tmin))
            print('tmax=' + str(tmax))
            # display temperature
            t=weather.get_temperature(forecast_input.day, forecast_input.hour)
            pcf8574.display_temperature(t)
            print('t=' + str(t))
            # display rain
            rain=weather.get_rain(forecast_input.day, forecast_input.hour)
            max7219.level = rain
            print('rain=' + str(rain))
            # display status
            status=weather.get_status(forecast_input.day, forecast_input.hour)
            pcf8574.display_status(status)
            print('status=' + str(status))
        except Exception as e:
            print('[main.py] Weather data not updated')

    time.sleep(1)
