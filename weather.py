# *************************************************************************************************** 
# ********************************************* WEATHER  ********************************************
# *************************************************************************************************** 
import importlib, os
import wlogging
from wlogging import LogType, LogMessage
from weatherAPIenum import WeatherConfig

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
def count_weather_apis():
    directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of main.py
    count = 0
    for filename in os.listdir(directory):
        if (filename.startswith('weatherAPI') and 
            not filename.startswith('weatherAPIenum') and 
            not filename.startswith('weatherAPIchange') and 
            os.path.isfile(os.path.join(directory, filename))):
            count += 1
    return count

MAX_APIS = count_weather_apis()
api_weather_id = 1

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
def get_weather_module(module_number):
    module_name = f"weatherAPI{module_number}"
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        print(f"Module {module_name} not found.")
        return None

def get_current_weather_api():
    """
    returns current weather api based on actived api_weather_id
    """
    global api_weather_id
    return get_weather_module(api_weather_id)

def get_current_weather_api_name():
    """
    returns current weather api name based on actived api_weather_id
    """
    weatherAPI = get_current_weather_api()
    return weatherAPI.api_name

def get_current_weather_api_refresh_s():
    """
    returns current weather api refresh time based on actived api_weather_id
    """
    weatherAPI = get_current_weather_api()
    return weatherAPI.api_refresh_s

# Change weather api
def change_weather_api():
    global api_weather_id
    if api_weather_id < MAX_APIS:
        api_weather_id += 1
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
