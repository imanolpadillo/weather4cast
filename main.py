import weatherAPI1
import max7219
import ky040
from time import strftime
import threading, time

def thread_weatherAPI(f_stop):
    print(strftime("%X"))
    if not f_stop.is_set():
        threading.Timer(10, thread_weatherAPI, [f_stop]).start()

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
# f_stop = threading.Event()
# thread_weatherAPI(f_stop)
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
    # print(ky040.counter)
    time.sleep(1)