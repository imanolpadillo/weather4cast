import weather
import max7219
import tm1637l
import ky040
from time import strftime
import threading, time

WEATHER_API_REFRESH_TIME = 1800 # in seconds
weather_refresh_flag = False

def thread_weatherAPI(f_stop):
    print('call weatherAPI' + str(weather.api_weather_id) + ': ' + strftime("%X"))
    weather.refresh()
    global weather_refresh_flag
    weather_refresh_flag = True
    if not f_stop.is_set():
        threading.Timer(WEATHER_API_REFRESH_TIME, thread_weatherAPI, [f_stop]).start()

thread_max7219_running = True
def thread_max7219_function():
    global thread_max7219_running
    while (thread_max7219_running):
        if max7219.message != "":
            max7219.show_message(max7219.message)
            max7219.message = ""
        else:
            max7219.show_level(max7219.level)
        time.sleep(max7219.timeout)

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
    if weather_refresh_flag == True:
        try:
            weather_refresh_flag = False
            # display min/max temperature
            [tmin,tmax]=weather.get_min_max_temperature(ky040.forecast_day)
            tm1637l.show_temperature(tmin,tmax)
            print('tmin=' + str(tmin))
            print('tmax=' + str(tmax))
            # display temperature
            t=weather.get_temperature(ky040.forecast_day, ky040.forecast_hour)
            print('t=' + str(t))
            # display rain
            rain=weather.get_rain(ky040.forecast_day, ky040.forecast_hour)
            print('rain=' + str(rain))
            # display status
            status=weather.get_status(ky040.forecast_day, ky040.forecast_hour)
            print('status=' + str(status))
        except Exception as e:
            print('[main.py] Weather data not updated')

    time.sleep(1)
