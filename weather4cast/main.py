#!/usr/bin/env python3
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
import wlogging
from wlogging import LogType, LogMessage
from weatherAPIenum import WeatherConfig, WeatherStatus, WeatherButton, WeatherTimeLine
 
# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
weather_refresh_flag = False
rain_warning_flag = False          # activated if it starts raining in following hours
check_rain_next_day_flag = True    # activated to check next day rain
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
# Thread that calls API weather every WEATHER_API_REFRESH_TIME seconds
def thread_weatherAPI(f_stop):
    log='API' + str(weather.api_weather_id) + ': ' + weather.get_current_weather_api_name() + \
                ', refresh_s: ' + str(weather.get_current_weather_api_refresh_s())
    wlogging.log(LogType.INFO.value,LogMessage.API_UPD.name, log)
    weather.refresh()
    global weather_refresh_flag
    weather_refresh_flag = True
    if not f_stop.is_set():
        threading.Timer(weather.get_current_weather_api_refresh_s(), thread_weatherAPI, [f_stop]).start()
 
# Thread that blink rain icon if it rains during current day
def thread_rainWarning(f_stop):
    global rain_warning_flag
    if rain_warning_flag == True:
        pcf8574.toggle_rain()
    if not f_stop.is_set():
        threading.Timer(WeatherConfig.RAIN_WARNING_REFRESH_TIME.value, thread_rainWarning, [f_stop]).start()
 
# Thread that updates max7219 led matrix
def thread_max7219_function():
    global thread_max7219_running
    while (thread_max7219_running):
        if max7219.message != "":
            max7219.show_message(max7219.message)
            max7219.message = ""
        else:
            max7219.show_level()
        time.sleep(max7219.timeout)
 
# Thread to change API when pushing button
def thread_changeAPI_function():
    global weather_refresh_flag
    global check_rain_next_day_flag  # disabled with double/tripple click
    while True:
        button_output = weatherAPIchange.detect_button()
        if button_output == WeatherButton.LongClick:
            change_weather_api(False)
        elif button_output == WeatherButton.SuperLongClick:
            reset_leds()
            change_weather_api(True)
        elif button_output == WeatherButton.ShortClick:
            weather.weather_timeline = WeatherTimeLine.T24
        elif button_output == WeatherButton.DoubleClick:
            pcf8574.tomorrow_rain(False)
            weather.weather_timeline = WeatherTimeLine.T48
        elif button_output == WeatherButton.TrippleClick:
            pcf8574.tomorrow_rain(False)
            weather.weather_timeline = WeatherTimeLine.T120
            
        # avoid button overlapping
        if button_output != WeatherButton.NoClick:
            weather_refresh_flag = True
            time.sleep(2)
        else:
            time.sleep(0.1) 
 
# ***************************************************************************************************
# FUNCTIONS
# ***************************************************************************************************
def reset_leds():
    """
    Deactivates and activates all leds, and set weather_api_id to 1
    """ 
    demo(True)
    time.sleep(3)
    demo(False)
 
def demo(flag):
    """
    Activates/deactivates all leds depending on flag value
    """
    max7219.demo(flag)
    pcf8574.demo(flag)
    tm1637l.demo(flag)
 
def show_api_error():
    """
    Deactivate all leds, except the message "api err" in tm1637
    """
    demo(False)
    tm1637l.show_api_error()
 
def change_weather_api(reset_api_id = False, refresh = True):
    global weather_refresh_flag
    global check_rain_next_day_flag
    check_rain_next_day_flag = True
    if reset_api_id == True:
        weather.api_weather_id = 0
    # Update weather_api_id
    weather.change_weather_api()
    # Display info about new api
    demo(False)
    tm1637l.show_api_name()
    if len(str(weather.api_weather_id))==1:
        max7219.message = '0' + str(weather.api_weather_id)
    else:
        max7219.message = str(weather.api_weather_id)
    time.sleep(max7219.timeout)
    if refresh == True:
    # Update api data
        weather.refresh()
        weather_refresh_flag = True
        # Log api update
        log = 'API' + str(weather.api_weather_id) + ': ' + weather.get_current_weather_api_name()+ \
            ', refresh_s: ' + str(weather.get_current_weather_api_refresh_s())
        wlogging.log(LogType.INFO.value,LogMessage.API_CHG.name,log)
 
def input_data_refresh():
    """
    Checks when control input changes (new day/hour)
    """
    change_flag = False
    global weather_refresh_flag
    global check_rain_next_day_flag
    global forecast_input
    global prev_forecast_input
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
        if int(now.strftime("%H")) == 0 and int(now.strftime("%M")) == 5 and int(now.strftime("%S")) == 0:
            check_rain_next_day_flag = True   # new day at 00:00:00
    else:
        forecast_input.hour = ky040.forecast_hour
 
    if forecast_input.dayFlag != prev_forecast_input.dayFlag:
        change_flag = True
        check_rain_next_day_flag = True   # change from today to select day and viceversa
    if forecast_input.hourFlag != prev_forecast_input.hourFlag:
        change_flag = True
    if forecast_input.hour != prev_forecast_input.hour:
        change_flag = True
    if forecast_input.dayFlag == True and (forecast_input.day != prev_forecast_input.day):
        change_flag = True
        check_rain_next_day_flag = True   # change day from select day
 
    if change_flag == True:
        log="day_flag=" + str(forecast_input.dayFlag) + \
              ", hour_flag=" + str(forecast_input.hourFlag) + \
              ", day=" + str(forecast_input.day) + ", hour=" + str(forecast_input.hour)
        wlogging.log(LogType.INFO.value,LogMessage.INDATA_CHG.name,log)
        weather_refresh_flag = True
 
    prev_forecast_input.dayFlag = forecast_input.dayFlag
    prev_forecast_input.hourFlag = forecast_input.hourFlag
    prev_forecast_input.day = forecast_input.day
    prev_forecast_input.hour = forecast_input.hour

def check_rain_next_day():
    """
    if 'check_rain_next_day_flag' is activated:
        - when day switch is changed
        - when day dial is modified with day switch activated
        - when day is changed with switches deactivated
    'get_rain_next_day()' is called to check if next day rains. In that case
    tomorrow_rain led is activated.
    """
    global check_rain_next_day_flag
    global forecast_input
    if check_rain_next_day_flag == True:
        check_rain_next_day_flag = False
        rain_flag = weather.get_rain_next_day(forecast_input.day, WeatherConfig.RAIN_WARNING_MM.value)
        pcf8574.tomorrow_rain(rain_flag)
        if rain_flag == True:
            wlogging.log(LogType.INFO.value,LogMessage.NEXTDAY_RAIN.name,LogMessage.NEXTDAY_RAIN.value)


# ***************************************************************************************************
# main
# ***************************************************************************************************
 
# start weatherAPI
weather.refresh()

# demo functionality for checking all leds
wlogging.log(LogType.INFO.value,LogMessage.SWITCH_ON.name,LogMessage.SWITCH_ON.value)
reset_leds()
change_weather_api(True, False)
 
# start threads
f_stop = threading.Event()
thread_weatherAPI(f_stop)
thread_rainWarning(f_stop)
 
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
            log=''
            # check if it rains next day
            check_rain_next_day()
            # lock rain_warning thread
            rain_warning_flag = False
            # text suffix
            suffix_24_48_120h = ''
            if weather.weather_timeline == WeatherTimeLine.T24:
                suffix_24_48_120h = '24'
            elif weather.weather_timeline == WeatherTimeLine.T48:
                suffix_24_48_120h = '48'
            elif weather.weather_timeline == WeatherTimeLine.T120:
                suffix_24_48_120h = '120'
            # display min/max temperature
            [tmin,tmax]=weather.get_min_max_temperature(forecast_input.day, weather.weather_timeline)
            tm1637l.show_temperature(tmin,tmax)
            log+='tmin=' + str(tmin) + '; tmax=' + str(tmax)
            # display temperature
            t=weather.get_temperature(forecast_input.day, forecast_input.hour, weather.weather_timeline)
            pcf8574.display_temperature(int(t))
            log+='; t' + suffix_24_48_120h + '=' + str(t)
            # display status
            status=weather.get_status(forecast_input.day, forecast_input.hour, weather.weather_timeline)
            pcf8574.display_status(status)
            log+='; status' + suffix_24_48_120h + '=' + str(status)
            # display rain
            rain=weather.get_rain(forecast_input.day, forecast_input.hour, weather.weather_timeline)
            max7219.calculate_level(rain,weather.weather_timeline)
            log+='; rain' + suffix_24_48_120h + '=' + str(rain)
            # display rain warning
            if weather.weather_timeline != WeatherTimeLine.T16 or status == WeatherStatus.RAINY or status == WeatherStatus.SNOWY or status == WeatherStatus.STORMY:
                rain_warning_flag = False     # do not blink rain status, if it is raining or snowing
            else:
                rain_warning_flag = weather.get_rain_warning(forecast_input.day,forecast_input.hour,
                                                             WeatherConfig.RAIN_WARNING_MM.value, WeatherConfig.RAIN_WARNING_TIME.value)
            log+='; rain_warning=' + str(rain_warning_flag)
            # logging
            wlogging.log(LogType.INFO.value,LogMessage.OUTDATA_CHG.name,log)
            # sleep in case of showing 24h/48h data
            if weather.weather_timeline != WeatherTimeLine.T16:
                weather.weather_timeline = WeatherTimeLine.T16
                weather_refresh_flag = True # required new loop for showing timeline 16h 
                time.sleep(5)
        except Exception as e:
            show_api_error()
            wlogging.log(LogType.ERROR.value,LogMessage.ERR_API_DATA.name,LogMessage.ERR_API_DATA.value + ': ' + str(e))
    time.sleep(0.5)
