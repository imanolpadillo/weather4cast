# *************************************************************************************************** 
# ********************************************* WEATHER  ********************************************
# *************************************************************************************************** 

import weatherAPI1, weatherAPI2, weatherAPI3, weatherAPI4, weatherAPI5, weatherAPI6
import wlogging
from wlogging import LogType, LogMessage
from weatherAPIenum import WeatherConfig

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
  
def get_rain_warning(forecast_day, forecast_hour, rain_limit, hour_limit):
    """
    returns true, if rain value is higher than rain_limit from next hour
    to the next amount of hours defined by hour_limit
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :rain_limit: mm that are considered as rain warning
    :hour_limit: hours to be monitored from forecast_day+forecast_hour
    :return: True if it rains the following hours
    """
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    weatherAPI = get_current_weather_api()
    # join all temperature values
    hour_counter=0
    rain_data = []
    for day in range(WeatherConfig.DAYS.value):
        for hour in range(24):
            rain_data.append(weatherAPI.weekWeather[day].rain[hour])
            hour_counter+=1
    # get current index
    index = forecast_day * 24 + forecast_hour

    # from index+1, check if it rains the following 'hour_limit' hours.
    hour_counter=0
    for hour in range(index + 1, len(rain_data)):
        if hour_counter>=hour_limit:
            return False
        if rain_data[hour] >= rain_limit:
            return True
        hour_counter+=1
    return False
