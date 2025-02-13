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
import lifx
from time import strftime
import threading, time
import pytz
from datetime import datetime, timedelta
import telegram
import wlogging
from wlogging import LogType, LogMessage
from weatherAPIenum import WeatherConfig, WeatherStatus, WeatherLifxScenes, \
WeatherButton, WeatherTimeLine, ActionButtonMode, WorkingMode
 
# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
weather_refresh_flag = False
rain_warning_flag = False          # activated if it starts raining in following hours
rain_warning_telegram_flag = False # if True telegram has already send
check_tomorrow_rain_flag = True    # activated to check tomorrow rain
disable_tomorrow_rain = False      # double click disable tomorrow rain
thread_max7219_running = True      # running thread for led matrix
eco_flag = WorkingMode.ON.value    # working mode: on, off or clock
eco_flag_change = False            # working mode changes
eco_off_manual_flag = False        # in manual eco_off, all leds are switched off until manual disabling
eco_clock_manual_flag = False      # in manual eco_clock, only time is enabled
last_status = None                 # if last_status != current_status, LIFX color changes
telegram_deadline  = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value)) # no telegram will be send until this deadline
action_button_mode = ActionButtonMode.Normal.value

 
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
# Thread that calls API weather
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
    if rain_warning_flag == True and not(weather.weather_timeline != WeatherTimeLine.T16 or 
                                         status == WeatherStatus.RAINY or status == WeatherStatus.SNOWY or 
                                         status == WeatherStatus.STORMY):
        pcf8574.toggle_rain(eco_flag == WorkingMode.ON.value)
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
 
# Thread to activate action button functionalities
def thread_actionButton_function():
    '''
    __  RST     : Reset system
    _   ECO     : Activate ECO
    ._  API+    : API change +1
    .._ API-    : API change -1
    .   0-24H   : Display 24H weather
    ..  24-48H  : Display tomorrow weather
    ... 24-120H : Display next 5 day weather
    '''
    global weather_refresh_flag
    global check_tomorrow_rain_flag  
    global disable_tomorrow_rain
    global eco_flag
    global eco_off_manual_flag
    global eco_clock_manual_flag
    global eco_flag_change
    global action_button_mode
    global forecast_input
    while True:
        # Wait until action button is pressed
        button_output = weatherAPIchange.detect_button()

        print(str(ky040.dayDial_click_times) + str(ky040.hourDial_click_times))
        # Get action mode
        if ky040.dayDial_click_times == 1 and ky040.hourDial_click_times == 0:
            action_button_mode = ActionButtonMode.IncreaseDayRel.value
        elif ky040.dayDial_click_times == 2 and ky040.hourDial_click_times == 0:
            action_button_mode = ActionButtonMode.IncreaseDayAbs.value
        elif ky040.dayDial_click_times == 0 and ky040.hourDial_click_times == 1:
            action_button_mode = ActionButtonMode.IncreaseHourRel.value
        elif ky040.dayDial_click_times == 0 and ky040.hourDial_click_times == 2:
            action_button_mode = ActionButtonMode.IncreaseHourAbs.value
        elif ky040.dayDial_click_times == 1 and ky040.hourDial_click_times == 1:
            if button_output == WeatherButton.LongClick:
                # LIFX neutral
                max7219.message = "LX"
                set_lifx_scene('NEUTRAL')
                button_output = WeatherButton.NoClick
            else:
                action_button_mode = ActionButtonMode.NextRain.value
        elif (ky040.dayDial_click_times == 1 and ky040.hourDial_click_times == 2) or + \
            (ky040.dayDial_click_times == 2 and ky040.hourDial_click_times == 1):
            # Rain report
            if button_output == WeatherButton.LongClick:
                max7219.message = "5R"
                send_telegram_rain_report(forecast_input.day, False)
            else:
                max7219.message = "1R"
                send_telegram_rain_report(forecast_input.day, True)
            button_output = WeatherButton.NoClick
        elif ky040.dayDial_click_times == 2 and ky040.hourDial_click_times == 2:
            # Weather report
            if button_output == WeatherButton.LongClick:
                max7219.message = "5W"
                send_telegram_weather_report(forecast_input.day, False)
            else:
                max7219.message = "1W"
                send_telegram_weather_report(forecast_input.day, True)
            button_output = WeatherButton.NoClick
        else:
            action_button_mode = ActionButtonMode.Normal.value
        
        # Reset dayDial and hourDial (because action button has been already pressed)
        ky040.dayDial_click_times = 0
        ky040.hourDial_click_times = 0

        # A) Action button: normal mode
        if action_button_mode == ActionButtonMode.Normal.value:
            if button_output == WeatherButton.x01ClickLongClick:
                # ._  API+    : API change +1
                # print('API+')
                change_weather_api(False, True, True)
            elif button_output == WeatherButton.x02ClickLongClick:
                # .._ API-    : API change -1
                # print('API-')
                change_weather_api(False, True, False)
            elif button_output == WeatherButton.LongClick:
                # _   ECO     : Activate ECO
                # print('ECO')
                demo(False)
                eco_off_manual_flag = True
                wlogging.log(LogType.INFO.value,LogMessage.MAN_MODE_OFF1.name,LogMessage.MAN_MODE_OFF1.value)
            elif button_output == WeatherButton.SuperLongClick:
                # __  RST     : Reset system
                # print('RST')
                reset_leds()
                change_weather_api(True)
            elif button_output == WeatherButton.x01Click:
                # .   0-24H   : Display 24H weather
                # print('0-24H')
                weather.weather_timeline = WeatherTimeLine.T24
            elif button_output == WeatherButton.x02Click:
                # ..  24-48H  : Display tomorrow weather
                # print('24-48H')
                if WeatherConfig.TOMORROW_RAIN_MANUAL_CANCEL.value:
                    disable_tomorrow_rain = True
                weather.weather_timeline = WeatherTimeLine.T48
            elif button_output == WeatherButton.x03Click:
                # ... 24-120H : Display next 5 day weather
                # print('24-120H')
                if WeatherConfig.TOMORROW_RAIN_MANUAL_CANCEL.value:
                    disable_tomorrow_rain = True
                weather.weather_timeline = WeatherTimeLine.T120
        # B) Action button: increase day relative
        elif action_button_mode == ActionButtonMode.IncreaseDayRel.value:
            weather.weather_timeline = WeatherTimeLine.T24
            # get init input day
            if switch.forecast_day_flag == False:
                forecast_input.day = 0
            else:
                forecast_input.day = ky040.forecast_day
            # increase input day sequentally
            if button_output == WeatherButton.x01Click:
                # +1 day
                forecast_input.day += 1
            elif button_output == WeatherButton.x02Click:
                # +2 days
                forecast_input.day += 2
            elif button_output == WeatherButton.x03Click:
                # +3 days
                forecast_input.day += 3
            elif button_output == WeatherButton.x04Click:
                # +4 days
                forecast_input.day += 4	
            elif button_output == WeatherButton.x05Click:
                # +5 days
                forecast_input.day += 5 
            elif button_output == WeatherButton.LongClick:
                # display weather API
                weather.weather_timeline = WeatherTimeLine.T16
                display_weather_api() 
            # trunc max forecast day
            if forecast_input.day >= WeatherConfig.DAYS.value:
                forecast_input.day = WeatherConfig.DAYS.value - 1
            # disable tomorrow rain when forecast day is tomorrow
            if forecast_input.day == 1: 
                if WeatherConfig.TOMORROW_RAIN_MANUAL_CANCEL.value:
                    disable_tomorrow_rain = True
            # display day name
            if button_output != WeatherButton.LongClick:
                day_name = max7219.calculate_week_day_name(forecast_input.day)
                max7219.message = str(day_name)
                time.sleep(1)
        # C) Action button: increase day absolute
        elif action_button_mode == ActionButtonMode.IncreaseDayAbs.value:
            weather.weather_timeline = WeatherTimeLine.T24
            if button_output == WeatherButton.x01Click:
                # Monday
                forecast_input.day = days_until_weekday(1)
            elif button_output == WeatherButton.x02Click:
                # Tuesday
                forecast_input.day = days_until_weekday(2)	
            elif button_output == WeatherButton.x03Click:
                # Wednesday
                forecast_input.day = days_until_weekday(3)
            elif button_output == WeatherButton.x04Click:
                # Thursday
                forecast_input.day = days_until_weekday(4)
            elif button_output == WeatherButton.x05Click:
                # Friday
                forecast_input.day = days_until_weekday(5)
            elif button_output == WeatherButton.x06Click:
                # Saturday
                forecast_input.day = days_until_weekday(6)	
            elif button_output == WeatherButton.x07Click:
                # Sunday
                forecast_input.day = days_until_weekday(7) 
            # display day name
            if button_output != WeatherButton.LongClick:
                day_name = max7219.calculate_week_day_name(forecast_input.day)
                max7219.message = str(day_name)
                time.sleep(1)
        # D) Action button: increase hour relative
        elif action_button_mode == ActionButtonMode.IncreaseHourRel.value: 
            if button_output == WeatherButton.LongClick:
                # Time mode
                action_button_mode = ActionButtonMode.Normal.value
                eco_clock_manual_flag = True  
                demo(False)
                weather.weather_timeline = WeatherTimeLine.T16
                # show date with manual flag
                tm1637l.show_date_time(WeatherConfig.INTENSITY_7LED_MODE_CLOCK.value, eco_clock_manual_flag)   
                wlogging.log(LogType.INFO.value,LogMessage.MAN_MODE_CLK1.name,LogMessage.MAN_MODE_CLK1.value) 
            else:
                current_hour = int(forecast_input.hour)
                forecast_input.hour=current_hour + button_output.value
                while forecast_input.hour > 24:
                    if forecast_input.day < WeatherConfig.DAYS.value - 1:
                        forecast_input.day += 1
                    forecast_input.hour = forecast_input.hour - 24
                if len(str(forecast_input.hour))==1:
                    max7219.message = '0' + str(forecast_input.hour)
                else:
                    max7219.message = str(forecast_input.hour)
        # E) Action button: increase hour absolute
        elif action_button_mode == ActionButtonMode.IncreaseHourAbs.value: 
            forecast_input.hour = int(button_output.value)
            while forecast_input.hour > 24:
                forecast_input.hour = forecast_input.hour - 24
            if len(str(forecast_input.hour))==1:
                max7219.message = '0' + str(forecast_input.hour)
            else:
                max7219.message = str(forecast_input.hour)
        # F) Action button: next rain
        elif action_button_mode == ActionButtonMode.NextRain.value:
            weather.weather_timeline = WeatherTimeLine.T16
            # Search start or end rain
            rain_start=True
            rain_index=0
            if button_output.value < 100:
                rain_start=True
                rain_index=button_output.value
            else:
                rain_start=False
                rain_index=button_output.value - 100
            
            forecast_input.day, forecast_input.hour = weather.get_next_start_stop_rain_hour(forecast_input.day, forecast_input.hour, rain_index, rain_start)
            
            if forecast_input.day == -1:
                # no next rain
                max7219.message = 'NO'
                button_output = WeatherButton.NoClick
                action_button_mode = ActionButtonMode.Normal.value
            else:
                if len(str(forecast_input.hour))==1:
                    max7219.message = '0' + str(forecast_input.hour)
                else:
                    max7219.message = str(forecast_input.hour)
        # avoid button overlapping
        if button_output != WeatherButton.NoClick and \
            not(button_output == WeatherButton.LongClick and action_button_mode == ActionButtonMode.Normal.value) and \
            not(button_output == WeatherButton.LongClick and action_button_mode == ActionButtonMode.IncreaseDayAbs.value):
            if eco_off_manual_flag == True:
                eco_flag_change = True
                eco_off_manual_flag = False
                wlogging.log(LogType.INFO.value,LogMessage.MAN_MODE_OFF0.name,LogMessage.MAN_MODE_OFF0.value)
            if eco_clock_manual_flag == True:
                eco_flag_change = True
                eco_clock_manual_flag = False
                wlogging.log(LogType.INFO.value,LogMessage.MAN_MODE_CLK0.name,LogMessage.MAN_MODE_CLK0.value)
            if eco_flag == WorkingMode.CLOCK.value or eco_flag == WorkingMode.OFF.value:
                eco_flag_change = True
            eco_flag = WorkingMode.ON.value
            pcf8574.tomorrow_rain(False)     # reset tomorrow rain
            check_tomorrow_rain_flag = True
            weather_refresh_flag = True
            time.sleep(2)
        else:
            time.sleep(0.1) 
 
# ***************************************************************************************************
# FUNCTIONS
# ***************************************************************************************************
def days_until_weekday(target_day):
    """
    Calculate the number of days from today until the given weekday.

    :param target_day: Integer representing the target weekday (Monday=1, ..., Sunday=7)
    :return: Number of days until the target weekday
    """
    # Get today's weekday (Monday=1, ..., Sunday=7)
    today = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value)).isoweekday()

    # Calculate the difference, accounting for wrapping around the week
    days_difference = (target_day - today) % 7

    # If the target day > 5, get the max available difference: 5
    if days_difference > 5:
        days_difference = 5

    return days_difference

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

def display_weather_api():
    demo(False)
    tm1637l.show_api_name()
    if len(str(weather.api_weather_id))==1:
        max7219.message = '0' + str(weather.api_weather_id)
    else:
        max7219.message = str(weather.api_weather_id)
    time.sleep(max7219.timeout)
 
def change_weather_api(reset_api_id = False, refresh = True, increase = True):
    global weather_refresh_flag
    global check_tomorrow_rain_flag
    check_tomorrow_rain_flag = True
    if reset_api_id == True:
        weather.api_weather_id = 0
    # Update weather_api_id
    weather.change_weather_api(increase)
    # Display info about new api
    display_weather_api()
    if refresh == True:
    # Update api data
        weather.refresh()
        weather_refresh_flag = True
        # Log api update
        log = 'API' + str(weather.api_weather_id) + ': ' + weather.get_current_weather_api_name()+ \
            ', refresh_s: ' + str(weather.get_current_weather_api_refresh_s())
        wlogging.log(LogType.INFO.value,LogMessage.API_CHG.name,log)

def get_eco_flag (current_date, current_day, current_hour):
    """
    check if current date is holiday
    check if current time is between eco scheduled init and end times
    """
    try:
        holidays = WeatherConfig.ECO_MODE_HOLIDAYS.value
        if (current_date.month, current_date.day) in holidays:
            value = WeatherConfig.ECO_MODE_HOLIDAYS_SCHEDULE.value[current_hour]
        else:
            # No holiday
            today_schedule = WeatherConfig.ECO_MODE_SCHEDULE.value[current_day]
            value = str(today_schedule[current_hour])
        return value
    except Exception as e:
        print(f"An error occurred: {e}")
        return WorkingMode.ON.value      # on
 
def input_data_refresh():
    """
    Checks when control input changes (new day/hour)
    """
    change_flag = False
    global weather_refresh_flag
    global check_tomorrow_rain_flag
    global forecast_input
    global prev_forecast_input
    global eco_flag
    switch.update()
    forecast_input.dayFlag = switch.forecast_day_flag
    forecast_input.hourFlag = switch.forecast_hour_flag
    if forecast_input.dayFlag == False:
        forecast_input.day = 0
    else:
        forecast_input.day = ky040.forecast_day
    if forecast_input.hourFlag == False:
        # Get the current time
        now = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))
        forecast_input.hour = now.strftime("%H")
        # Reset check_tomorrow_rain_flag at 00:00:00
        if int(now.strftime("%H")) == 0 and int(now.strftime("%M")) == 0 and int(now.strftime("%S")) == 0:
            check_tomorrow_rain_flag = True   # new day at 00:00:00
    else:
        forecast_input.hour = ky040.forecast_hour
 
    if forecast_input.dayFlag != prev_forecast_input.dayFlag:
        change_flag = True
        check_tomorrow_rain_flag = True   # change from today to select day and viceversa
    if forecast_input.hourFlag != prev_forecast_input.hourFlag:
        change_flag = True
    if forecast_input.hour != prev_forecast_input.hour:
        change_flag = True
    if forecast_input.dayFlag == True and (forecast_input.day != prev_forecast_input.day):
        change_flag = True
        check_tomorrow_rain_flag = True   # change day from select day
 
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

def check_tomorrow_rain(weather_timeline = WeatherTimeLine.T16):
    """
    if 'check_tomorrow_rain_flag' is activated:
        - when day switch is changed
        - when day dial is modified with day switch activated
        - when day is changed with switches deactivated
    'get_rain_next_day()' is called to check if next day rains. In that case
    tomorrow_rain led is activated.
    returns:
        - 'Disabled': when user doble/triple clicked action button
        - 'True': tomorrow rains
        - 'False': tomorrow does not rain
    """
    global check_tomorrow_rain_flag
    global forecast_input
    rain_flag = 'Disabled'
    forecast_day = forecast_input.day
    if weather_timeline==WeatherTimeLine.T48:
        # For T48, the rain check must be for next day
        if forecast_day<WeatherConfig.DAYS.value-1: forecast_day += 1
    elif weather_timeline==WeatherTimeLine.T120:
        # For T120, no light is displayed
        return str(rain_flag)
    if check_tomorrow_rain_flag == True:
        rain_flag = weather.get_tomorrow_rain(forecast_day, WeatherConfig.RAIN_WARNING_MM.value)
        pcf8574.tomorrow_rain(rain_flag)
    return str(rain_flag)

def add_hours_to_current_time(hours):
    """
    Generate a date that adds input(hours) to current date
    """    
    # Get the current date and time
    current_time = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))
    
    # Create a timedelta object representing the hours to add
    time_delta = timedelta(hours=hours)
    
    # Add the timedelta to the current time
    new_time = current_time + time_delta
    
    return new_time

def set_lifx_scene(scene):
    """
    Change LIFX color 
    """     
    try:
        #lifx.set_lifx_color(*WeatherLifxColor[scene].value)
        lifx.set_lifx_scene(WeatherLifxScenes[scene].value)
        wlogging.log(LogType.INFO.value,LogMessage.LIFX_CHG.name,str(scene))
    except:
        wlogging.log(LogType.ERROR.value,LogMessage.ERR_LIFX.name,LogMessage.ERR_LIFX.value)

def send_telegram_rain_warning(hour, rain_warning_quantity):
    """
    Send telegram indicating rain warning for following hours
    """   
    message = ''
    for index, value in enumerate(rain_warning_quantity):
        rain_hour = int(hour) + index 
        # pass from 23h to 00h
        while rain_hour >= 24:
            rain_hour -= 24
        # hour always with 2 digits
        rain_hour_str = str(rain_hour).zfill(2)
        message += '\n' + rain_hour_str + 'h: ' + str(value) + 'mm/h'
    telegram.send_telegram(f"[RAIN WARNING]: {message}" )
    wlogging.log(LogType.INFO.value,LogMessage.TELEGRAM_SND.name,LogMessage.TELEGRAM_SND.value)

def send_telegram_rain_report(day, one_day = True):
    """
    Send telegram indicating the hours with rain
    """   
    if one_day == True:
        day_name = max7219.calculate_week_day_name(day)
        report = weather.get_rain_report(day)
        telegram.send_telegram(f"[RAIN REPORT FOR {day_name}]: {report}")
    else:
        message = ''
        for day in range(WeatherConfig.DAYS.value):
            day_name = max7219.calculate_week_day_name(day)
            report = weather.get_rain_report(day)
            message += f"[RAIN REPORT FOR {day_name}]: {report}" + '\n\n'
        telegram.send_telegram(message)    
    wlogging.log(LogType.INFO.value,LogMessage.TELEGRAM_SND.name,LogMessage.TELEGRAM_SND.value)

def send_telegram_weather_report(day, one_day = True):
    """
    Send telegram indicating the rain + temperature + status for input day
    """   
    if one_day == True:
        day_name = max7219.calculate_week_day_name(day)
        report = weather.get_weather_report(day)
        telegram.send_telegram(f"[WEATHER REPORT FOR {day_name}]: {report}")
    else:
        message = ''
        for day in range(WeatherConfig.DAYS.value -1):   #1day less to avoid max telegram lenght
            day_name = max7219.calculate_week_day_name(day)
            report = weather.get_weather_report(day)
            message += f"[WEATHER REPORT FOR {day_name}]: {report}" + '\n\n'
        telegram.send_telegram(message)    
    wlogging.log(LogType.INFO.value,LogMessage.TELEGRAM_SND.name,LogMessage.TELEGRAM_SND.value)

# ***************************************************************************************************
# main
# ***************************************************************************************************
 
# start weatherAPI
weather.refresh()

# demo functionality for checking all leds
wlogging.log(LogType.INFO.value,LogMessage.SWITCH_ON.name,LogMessage.SWITCH_ON.value)
reset_leds()
change_weather_api(True, False)

# get init mode
now = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))
eco_flag = get_eco_flag(now.today(),now.weekday(),now.time().hour)
weather_refresh_flag = True
 
# start threads
f_stop = threading.Event()
thread_weatherAPI(f_stop)
thread_rainWarning(f_stop)
 
thread_max7219 = threading.Thread(target=thread_max7219_function)
thread_max7219.start()
 
thread_actionButton = threading.Thread(target=thread_actionButton_function)
thread_actionButton.start()

# reset leds
time.sleep(2)
demo(False)
 
# infinite loop
while True:
    # in normal mode, day is set by input controls
    if action_button_mode == ActionButtonMode.Normal.value:
        input_data_refresh()

    # Check eco_mode every 5 minutes
    if WeatherConfig.ECO_MODE_ON.value == True:
        now = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))
        if int(now.strftime("%M")) % 5 == 0 and int(now.strftime("%S")) == 0: 
            prev_eco_flag = eco_flag 
            eco_flag = get_eco_flag(now.today(),now.weekday(),now.time().hour)
            if prev_eco_flag != eco_flag or eco_flag_change:
                eco_flag_change = True
                weather_refresh_flag = True
    else:
        eco_flag = WorkingMode.ON.value

    # A) OFF MODE
    if eco_off_manual_flag == True or (eco_flag == WorkingMode.OFF.value and weather_refresh_flag == True):
        # reset all leds
        if eco_flag_change:
            demo(False)
        weather_refresh_flag = False
        # logging working mode
        if eco_flag_change:
            eco_flag_change = False
            wlogging.log(LogType.INFO.value,LogMessage.ECO_MODE_OFF.name,LogMessage.ECO_MODE_OFF.value)
    # B) CLOCK MODE
    elif eco_clock_manual_flag == True or (eco_flag == WorkingMode.CLOCK.value):
        if (int(now.strftime("%M")) % 1 == 0 and int(now.strftime("%S")) == 0) or weather_refresh_flag == True: 
            # enable only time
            if eco_flag_change == True:
                demo(False)
            # show date with manual flag
            tm1637l.show_date_time(WeatherConfig.INTENSITY_7LED_MODE_CLOCK.value, eco_clock_manual_flag)   
            weather_refresh_flag = False
        # logging working mode
        if eco_flag_change:
            eco_flag_change = False
            wlogging.log(LogType.INFO.value,LogMessage.ECO_MODE_CLK.name,LogMessage.ECO_MODE_CLK.value)
    # C) ON MODE
    elif eco_flag == WorkingMode.ON.value and weather_refresh_flag == True:
        try:
            weather_refresh_flag = False
            log=''
            # logging working mode
            if eco_flag_change:
                eco_flag_change = False
                wlogging.log(LogType.INFO.value,LogMessage.ECO_MODE_ON.name,LogMessage.ECO_MODE_ON.value)
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
            log+='tmin' + suffix_24_48_120h + '=' + str(tmin) + '; tmax' + suffix_24_48_120h + '=' + str(tmax)
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
            max7219.calculate_level(rain, weather.weather_timeline, action_button_mode, forecast_input.day, forecast_input.hourFlag, forecast_input.hour)
            log+='; rain' + suffix_24_48_120h + '=' + str(rain)
            # display rain warning
            rain_warning_flag, rain_warning_quantity, rain_hour_counter = weather.get_rain_warning(forecast_input.day,forecast_input.hour,
                                                                                    WeatherConfig.RAIN_WARNING_MM.value, WeatherConfig.RAIN_WARNING_TIME.value,
                                                                                    weather.weather_timeline)
            log+='; rain_warning' + suffix_24_48_120h + '=' + str(rain_warning_flag)
            # display tomorrow rain
            tomorrow_rain = check_tomorrow_rain(weather.weather_timeline)
            log+='; tomorrow_rain' + suffix_24_48_120h + '=' + str(tomorrow_rain)
            # send rain warning notification
            if WeatherConfig.RAIN_WARNING_TELEGRAM_ON.value == True:
                if weather.weather_timeline == WeatherTimeLine.T16 and switch.forecast_day_flag == False and switch.forecast_hour_flag == False and action_button_mode != ActionButtonMode.NextRain.value:
                    if rain_warning_flag == True: 
                        if rain_warning_telegram_flag == False:
                            send_telegram_rain_warning(forecast_input.hour, rain_warning_quantity)
                            telegram_deadline = add_hours_to_current_time(rain_hour_counter)
                            rain_warning_telegram_flag = True
                    else:
                        # avoid sending multiple telegram messages for same rain
                        if datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))>telegram_deadline:
                            rain_warning_telegram_flag = False
            # change lifx color
            if WeatherConfig.LIFX_ON.value == True and status != last_status:
                last_status = status
                set_lifx_scene(status.name)
            # logging
            wlogging.log(LogType.INFO.value,LogMessage.OUTDATA_CHG.name,log)
            # sleep in case of showing 24h/48h data
            if weather.weather_timeline != WeatherTimeLine.T16 or \
                action_button_mode == ActionButtonMode.IncreaseHourAbs.value or \
                action_button_mode == ActionButtonMode.IncreaseHourRel.value or \
                action_button_mode == ActionButtonMode.NextRain.value:
                weather.weather_timeline = WeatherTimeLine.T16
                weather_refresh_flag = True # required new loop for showing timeline 16h 
                time.sleep(WeatherConfig.TIMEOUT_24_48_120.value)
                pcf8574.tomorrow_rain(False)       # switch off tomorrow rain
                if disable_tomorrow_rain == True:
                    disable_tomorrow_rain = False
                    check_tomorrow_rain_flag = False
                else:
                    check_tomorrow_rain_flag = True
            # reset action button
            action_button_mode = ActionButtonMode.Normal.value
        except Exception as e:
            show_api_error()
            wlogging.log(LogType.ERROR.value,LogMessage.ERR_API_DATA.name,LogMessage.ERR_API_DATA.value + ': ' + str(e))
    time.sleep(0.5)
