# *************************************************************************************************** 
# ********************************************* WEATHER  ********************************************
# *************************************************************************************************** 

import weatherAPI1, weatherAPI2

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

api_weather_id = 1

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
        else:
            data = weatherAPI2.call_api()
            weatherAPI2.decode_json(data)    
    except Exception as e:
        print('[weather.py] API error')    

def get_min_max_temperature (forecast_day):
    """
    gets min and max temperature of input forecast day
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :return: [tmin,tmax]
    """
    if api_weather_id == 1:
        tmin = min(list(map(int, weatherAPI1.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI1.weekWeather[forecast_day].temperature)))
    else:
        tmin = min(list(map(int, weatherAPI2.weekWeather[forecast_day].temperature)))
        tmax = max(list(map(int, weatherAPI2.weekWeather[forecast_day].temperature)))    
    return [tmin, tmax]

def get_temperature (forecast_day, forecast_hour):
    """
    gets temperature of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    if api_weather_id == 1:
        return weatherAPI1.weekWeather[forecast_day].temperature[forecast_hour]
    else:
        return weatherAPI2.weekWeather[forecast_day].temperature[forecast_hour]    

def get_rain (forecast_day, forecast_hour):
    """
    gets rain of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    if api_weather_id == 1:
        return weatherAPI1.weekWeather[forecast_day].rain[forecast_hour]
    else:
        return weatherAPI2.weekWeather[forecast_day].rain[forecast_hour]

def get_status (forecast_day, forecast_hour):
    """
    gets status of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    if api_weather_id == 1:
        return weatherAPI1.weekWeather[forecast_day].status[forecast_hour]
    else:
        return weatherAPI2.weekWeather[forecast_day].status[forecast_hour]
  