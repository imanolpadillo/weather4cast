# *************************************************************************************************** 
# ************************************** WEATHER API: DUMMY *****************************************
# *************************************************************************************************** 

from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
 
api_name = 'dummy'
api_refresh_s = 900

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  # today + tomorrow + next days

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def refresh():
    """
    refresh dummy data
    """
    try:
        global weekWeather
        weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  

        for i in range(24):
            weekWeather[0].rain[i] = 0
            weekWeather[0].temperature[i] = 0
            weekWeather[0].status[i] = WeatherStatus.SUNNY

        for i in range(24):
            weekWeather[1].rain[i] = 0.5
            weekWeather[1].temperature[i] = 1
            weekWeather[1].status[i] = WeatherStatus.CLOUDY

        for i in range(24):
            weekWeather[2].rain[i] = 1
            weekWeather[2].temperature[i] = 2
            weekWeather[2].status[i] = WeatherStatus.FOGGY

        for i in range(24):
            weekWeather[3].rain[i] = 1.5
            weekWeather[3].temperature[i] = 3
            weekWeather[3].status[i] = WeatherStatus.STORMY

        for i in range(24):
            weekWeather[4].rain[i] = 2
            weekWeather[4].temperature[i] = 4
            weekWeather[4].status[i] = WeatherStatus.SNOWY

        for i in range(24):
            weekWeather[5].rain[i] = 2.5
            weekWeather[5].temperature[i] = 5
            weekWeather[5].status[i] = WeatherStatus.WINDY
            
    except Exception as e:
        wlogging.log(LogType.ERROR.value, LogMessage.ERR_API_CONN.name, LogMessage.ERR_API_CONN.value + ': ' + str(e))

# refresh() # get data first time
# print("DUMMY")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)
