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

def refresh():
    """
    calls REST-API and converts json into appropiate information for global variable
    'weekStatus'
    """
    try:
        if api_weather_id == 1:
            data = weatherAPI1.call_api()
            weatherAPI1.decode_json(data)
        elif api_weather_id == 2:
            data = weatherAPI2.call_api()
            weatherAPI2.decode_json(data)
        elif api_weather_id == 3:
            data = weatherAPI3.call_api()
            weatherAPI3.decode_json(data)
        elif api_weather_id == 4:
            data = weatherAPI4.call_api()
            weatherAPI4.decode_json(data)
        elif api_weather_id == 5:
            data = weatherAPI5.call_api()
            weatherAPI5.decode_json(data)
        else:
            data = weatherAPI6.call_api()
            weatherAPI6.decode_json(data)    
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

def get_min_max_temperature (forecast_day):
    """
    gets min and max temperature of input forecast day
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :return: [tmin,tmax]
    """
    if api_weather_id == 1:
        tmin = min(list(map(int, weatherAPI1.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI1.weekWeather[forecast_day].temperature)))
    elif api_weather_id == 2:
        tmin = min(list(map(int, weatherAPI2.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI2.weekWeather[forecast_day].temperature))) 
    elif api_weather_id == 3:
        tmin = min(list(map(int, weatherAPI3.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI3.weekWeather[forecast_day].temperature)))
    elif api_weather_id == 4:
        tmin = min(list(map(int, weatherAPI4.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI4.weekWeather[forecast_day].temperature)))
    elif api_weather_id == 5:
        tmin = min(list(map(int, weatherAPI5.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI5.weekWeather[forecast_day].temperature)))
    else:
        tmin = min(list(map(int, weatherAPI6.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI6.weekWeather[forecast_day].temperature)))    
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
    if api_weather_id == 1:
        return weatherAPI1.weekWeather[forecast_day].temperature[forecast_hour]
    elif api_weather_id == 2:
        return weatherAPI2.weekWeather[forecast_day].temperature[forecast_hour]
    elif api_weather_id == 3:
        return weatherAPI3.weekWeather[forecast_day].temperature[forecast_hour]
    elif api_weather_id == 4:
        return weatherAPI4.weekWeather[forecast_day].temperature[forecast_hour]
    elif api_weather_id == 5:
        return weatherAPI5.weekWeather[forecast_day].temperature[forecast_hour]    
    else:
        return weatherAPI6.weekWeather[forecast_day].temperature[forecast_hour]  

def get_rain (forecast_day, forecast_hour):
    """
    gets rain of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    if api_weather_id == 1:
        return weatherAPI1.weekWeather[forecast_day].rain[forecast_hour]
    elif api_weather_id == 2:
        return weatherAPI2.weekWeather[forecast_day].rain[forecast_hour]
    elif api_weather_id == 3:
        return weatherAPI3.weekWeather[forecast_day].rain[forecast_hour]
    elif api_weather_id == 4:
        return weatherAPI4.weekWeather[forecast_day].rain[forecast_hour]
    elif api_weather_id == 5:
        return weatherAPI5.weekWeather[forecast_day].rain[forecast_hour]
    else:
        return weatherAPI6.weekWeather[forecast_day].rain[forecast_hour]

def get_status (forecast_day, forecast_hour):
    """
    gets status of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    if api_weather_id == 1:
        return weatherAPI1.weekWeather[forecast_day].status[forecast_hour]
    elif api_weather_id == 2:
        return weatherAPI2.weekWeather[forecast_day].status[forecast_hour]
    elif api_weather_id == 3:
        return weatherAPI3.weekWeather[forecast_day].status[forecast_hour]
    elif api_weather_id == 4:
        return weatherAPI4.weekWeather[forecast_day].status[forecast_hour]
    elif api_weather_id == 5:
        return weatherAPI5.weekWeather[forecast_day].status[forecast_hour]
    else:
        return weatherAPI6.weekWeather[forecast_day].status[forecast_hour]
  