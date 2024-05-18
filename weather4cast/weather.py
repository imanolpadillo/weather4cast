# *************************************************************************************************** 
# ********************************************* WEATHER  ********************************************
# *************************************************************************************************** 
import importlib, os, math
from weatherAPIenum import WeatherConfig, RainTimeLine

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
weatherAPI = None
api_weather_id = 1
# weatherAPI files are ordered alphabetically, and file names are saved in the following array.
weatherAPInames = []
weather_rain_timeline = RainTimeLine.T16

def count_weather_apis():
    global weatherAPInames
    directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of main.py
    count = 0
    for filename in sorted(os.listdir(directory)):
        if (filename.startswith('weatherAPI') and 
            not filename.startswith('weatherAPIenum') and 
            not filename.startswith('weatherAPIchange') and 
            os.path.isfile(os.path.join(directory, filename))):
            weatherAPInames.append(filename.split('.')[0]) # remove suffiy
            count += 1
    return count

MAX_APIS = count_weather_apis()

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
def get_weather_api_module(weather_api_index):
    global weatherAPInames
    module_name = weatherAPInames[weather_api_index-1]
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
    return get_weather_api_module(api_weather_id)

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
        global weatherAPI
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
    global weatherAPI
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
    global weatherAPI
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    return weatherAPI.weekWeather[forecast_day].temperature[forecast_hour]

def get_rain (forecast_day, forecast_hour, rain_time_line):
    """
    gets rain from input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    global weatherAPI
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    hour_counter=0
    rain_data = []
    for day in range(WeatherConfig.DAYS.value):
        # for hour in range(24):
        for hour in range(len(weatherAPI.weekWeather[day].rain)):
            rain_data.append(weatherAPI.weekWeather[day].rain[hour])
            hour_counter+=1
    # get current index
    index=0
    hour_limit=0
    if rain_time_line==RainTimeLine.T16:
        hour_limit=16
        index = forecast_day * 24 + forecast_hour
    else:
        hour_limit=24
        index = forecast_day * 24
    
    # from index count 16 or 24 rain values
    rain_output = []
    for hour in range(index, len(rain_data)):
        if hour>=hour_limit+index:
            break
        rain_output.append(rain_data[hour])

    # fill with '0.0' if array´s size is lower than hour limit
    while(len(rain_output)<hour_limit):
        rain_output.append(0.0)

    # adjust rain array to size 16
    if len(rain_output)==RainTimeLine.T24.value:
        rain_output = rain_24_to_16_hours(rain_output)

    return rain_output

def ceil_half(value):
    # Check if the fractional part is strictly greater than 0.5
    if value % 1 > 0.5:
        return math.ceil(value)
    # Check if the value is exactly 0.5 or 1.0
    elif value % 1 == 0.5 or value % 1 == 0:
        return value
    # For all other cases, round up to the nearest half-integer
    else:
        return math.ceil(value * 2) / 2

def rain_24_to_16_hours(input_array):
    """
    converts 24 array into 16 array
    :param input_array: size 24
    :return: array size 16
    """
    if len(input_array) != 24:
        raise ValueError("Input array must have 24 elements.")
    output_array = []
    for i in range(0, len(input_array), 3):
        # Calculate the average of each pair of 1.5 groups
        avg1 = ceil_half((input_array[i] + input_array[i+1]) / 2)
        avg2 = ceil_half((input_array[i+1] + input_array[i+2]) / 2)
        output_array.extend([avg1, avg2])
    return output_array

def get_status (forecast_day, forecast_hour):
    """
    gets status of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: [tmin,tmax]
    """
    global weatherAPI
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
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
    global weatherAPI
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    # join all temperature values
    hour_counter=0
    rain_data = []
    for day in range(WeatherConfig.DAYS.value):
        # for hour in range(24):
        for hour in range(len(weatherAPI.weekWeather[day].rain)):
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
