import weatherAPI
from time import strftime
import threading, time

def thread_weatherAPI(f_stop):
    print(strftime("%X"))
    if not f_stop.is_set():
        threading.Timer(10, thread_weatherAPI, [f_stop]).start()

# start calling f now and every 60 sec thereafter
f_stop = threading.Event()
thread_weatherAPI(f_stop)
time.sleep(60)
f_stop.set()

# weatherAPI.refresh()
# print(weatherAPI.weekWeather[0].status)
# print(strftime("%X"))