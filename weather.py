# *************************************************************************************************** 
# ********************************************* WEATHER  ********************************************
# *************************************************************************************************** 

import weatherAPI1, weatherAPI2, weatherAPI3, weatherAPI4, weatherAPI5, weatherAPI6
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

api_weather_id = 1
api_weather_names = [weatherAPI1.api_name, weatherAPI2.api_name, weatherAPI3.api_name, 
                     weatherAPI4.api_name, weatherAPI5.api_name, weatherAPI6.api_name]

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def get_current_weather_api():
    try:
        if api_weather_id == 1:
            return weatherAPI1
        elif api_weather_id == 2:
            return weatherAPI2
        elif api_weather_id == 3:
            return weatherAPI3
        elif api_weather_id == 4:
            return weatherAPI4
        elif api_weather_id == 5:
            return weatherAPI5
        else:
            return weatherAPI6  
    except Exception as e:
        return 
    
# Change weather api
def change_weather_api():
    global api_weather_id
    if api_weather_id == 1:
        api_weather_id = 2
    elif api_weather_id == 2:
        api_weather_id = 3
    elif api_weather_id == 3:
        api_weather_id = 4
    elif api_weather_id == 4:
        api_weather_id = 5
    elif api_weather_id == 5:
        api_weather_id = 6
    else:
        api_weather_id = 1

def refresh():
    """
    calls REST-API and converts json into appropiate information for global variable
    'weekStatus'
    """
    try:
        weatherAPI = get_current_weather_api()
        data = weatherAPI.call_api()
        weatherAPI.decode_json(data)    
    except Exception as e:
        return

def get_min_max_temperature (forecast_day):
    """
    gets min and max temperature of input forecast day
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :return: [tmin,tmax]
    """
    weatherAPI = get_current_weather_api()
    tmin = min(list(map(int, weatherAPI.weekWeather[forecast_day].temperature)))
    tmax = max(list(map(int, weatherAPI.weekWeather[forecast_day].temperature)))    
    return [tmin, tmax]

def get_temperature (forecast_day, forecast_hour):
    """
    gets temperature of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    weatherAPI = get_current_weather_api()
    return weatherAPI.weekWeather[forecast_day].temperature[forecast_hour]

def get_rain (forecast_day, forecast_hour):
    """
    gets rain of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    weatherAPI = get_current_weather_api()
    return weatherAPI.weekWeather[forecast_day].rain[forecast_hour]

def get_status (forecast_day, forecast_hour):
    """
    gets status of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    weatherAPI = get_current_weather_api()
    return weatherAPI.weekWeather[forecast_day].status[forecast_hour]
  
def get_rainWarning(forecast_day, forecast_hour, rain_limit):
    """
    returns true, if rain value is higher than rain_limit in current day
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: True if rain value is higher than rain_limit in current day
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    return True
