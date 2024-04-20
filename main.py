# *************************************************************************************************** 
# ************************************************ MAIN *********************************************
# *************************************************************************************************** 
import weather
import max7219
import tm1637l
import ky040
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

class ForecastData:
    def __init__(self, dayFlag=False, hourFlag=False, day=0, hour=0):
        self.dayFlag = dayFlag
        self.hourFlag = hourFlag
        self.day = day
        self.hour = hour
forecast_data = ForecastData()
prev_forecast_data = ForecastData()

# *************************************************************************************************** 
# FUNCTIONS
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

def input_data_refresh():
    change_flag = False
    global weather_refresh_flag
    switch.update()
    forecast_data.dayFlag = switch.forecast_day_flag
    forecast_data.hourFlag = switch.forecast_hour_flag
    if forecast_data.dayFlag == False:
        forecast_data.day = 0
    else:
        forecast_data.day = ky040.forecast_day
    if forecast_data.hourFlag == False:
        # Get the timezone for Madrid
        madrid_tz = pytz.timezone('Europe/Madrid')
        now = datetime.now(madrid_tz)
        forecast_data.hour = now.strftime("%H")
    else:
        forecast_data.hour = ky040.forecast_hour

    if forecast_data.dayFlag != prev_forecast_data.dayFlag:
        change_flag = True
    if forecast_data.hourFlag != prev_forecast_data.hourFlag:
        change_flag = True
    if forecast_data.hour != prev_forecast_data.hour:
        change_flag = True
    if forecast_data.dayFlag == True and (forecast_data.day != prev_forecast_data.day):
        change_flag = True

    if change_flag == True:
        print("INPUT_DATA: day_flag=" + str(forecast_data.dayFlag) + ", hour_flag=" + str(forecast_data.hourFlag) + \
              ", day=" + str(forecast_data.day) + ", hour=" + str(forecast_data.hour))
        weather_refresh_flag = True

    prev_forecast_data.dayFlag = forecast_data.dayFlag
    prev_forecast_data.hourFlag = forecast_data.hourFlag
    prev_forecast_data.day = forecast_data.day
    prev_forecast_data.hour = forecast_data.hour


# *************************************************************************************************** 
# main
# *************************************************************************************************** 

# start calling f now and every 60 sec thereafter
f_stop = threading.Event()
thread_weatherAPI(f_stop)
# time.sleep(60)
# f_stop.set()

# weatherAPI.refresh()
# print(weatherAPI.weekWeather[0].status)
# print(strftime("%X"))

thread_max7219 = threading.Thread(target=thread_max7219_function)
thread_max7219.start()
# time.sleep(2)
# max7219.level=1
# time.sleep(2)
# max7219.level=2
# time.sleep(2)
# max7219.message="23"
# time.sleep(2)
# max7219.level=3
# time.sleep(2)
# thread_max7219_running = False
# thread_max7219.join()
# print("end")

while True:
    input_data_refresh()
    if weather_refresh_flag == True:
        try:
            weather_refresh_flag = False
            # display min/max temperature
            [tmin,tmax]=weather.get_min_max_temperature(forecast_data.day)
            tm1637l.show_temperature(tmin,tmax)
            print('tmin=' + str(tmin))
            print('tmax=' + str(tmax))
            # display temperature
            t=weather.get_temperature(forecast_data.day, forecast_data.hour)
            print('t=' + str(t))
            # display rain
            rain=weather.get_rain(forecast_data.day, forecast_data.hour)
            print('rain=' + str(rain))
            # display status
            status=weather.get_status(forecast_data.day, forecast_data.hour)
            print('status=' + str(status))
        except Exception as e:
            print('[main.py] Weather data not updated')

    time.sleep(1)
