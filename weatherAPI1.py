# *************************************************************************************************** 
# ****************************************** WEATHER API1 *******************************************
# *************************************************************************************************** 
# Source: https://open-meteo.com/en/docs

import requests,math
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
 
api_url = 'https://api.open-meteo.com/v1/forecast?latitude=42.85&longitude=-2.6727&hourly=apparent_temperature,rain,weather_code,wind_speed_10m&timezone=auto'
api_name = 'openmet '

dict_weather_status = [
                       {0: WeatherStatus.SUNNY}, \
                       {1: WeatherStatus.SUNNY}, \
                       {2: WeatherStatus.PARTLY_CLOUDY}, \
                       {3: WeatherStatus.CLOUDY}, \
                       {45: WeatherStatus.FOGGY}, \
                       {48: WeatherStatus.FOGGY}, \
                       {51: WeatherStatus.RAINY}, \
                       {53: WeatherStatus.RAINY}, \
                       {55: WeatherStatus.RAINY}, \
                       {56: WeatherStatus.RAINY}, \
                       {57: WeatherStatus.RAINY}, \
                       {61: WeatherStatus.RAINY}, \
                       {63: WeatherStatus.RAINY}, \
                       {65: WeatherStatus.RAINY}, \
                       {66: WeatherStatus.RAINY}, \
                       {67: WeatherStatus.RAINY}, \
                       {71: WeatherStatus.SNOWY}, \
                       {73: WeatherStatus.SNOWY}, \
                       {75: WeatherStatus.SNOWY}, \
                       {77: WeatherStatus.SNOWY}, \
                       {80: WeatherStatus.RAINY}, \
                       {81: WeatherStatus.RAINY}, \
                       {82: WeatherStatus.RAINY}, \
                       {85: WeatherStatus.SNOWY}, \
                       {86: WeatherStatus.SNOWY}, \
                       {95: WeatherStatus.STORMY}, \
                       {96: WeatherStatus.STORMY}, \
                       {99: WeatherStatus.STORMY}, \
                       {100: WeatherStatus.WINDY}
                    ]

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  # today + tomorrow + next days

MAX_WIND_KMH = 50

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

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
    

def call_api():
    """
    calls REST-API from "api.open-meteo.com"
    :return: json file
    """ 
    url = api_url
    headers = {'cache-control': "no-cache"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def decode_json(data):
    """
    calls REST-API from "api.open-meteo.com". Global variable "weekWeather" is updated.
    :param data: json file obtained from "el-tiempo.net" REST-API
    :return: -
    """ 
    global weekWeather
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value+1)]  
    count = 0
    for day in range(WeatherConfig.DAYS.value):
        for hour in range(24):
            weekWeather[day].temperature[hour] = round(data['hourly']['apparent_temperature'][count])
            weekWeather[day].rain[hour] = ceil_half(data['hourly']['rain'][count])
            if (data['hourly']['wind_speed_10m'][count]>MAX_WIND_KMH):
                #wind status is not defined in 'weather code'
                weekWeather[day].status[hour] = 100 # windy code
            else:
                weekWeather[day].status[hour] = data['hourly']['weather_code'][count]
            count+=1  
   
    # Decode weather status
    for x in range(len(weekWeather)):
        for ycount, yvalue in enumerate(weekWeather[x].status):
            weekWeather[x].status[ycount] = decode_weather_status(weekWeather[x].status[ycount], dict_weather_status)


def decode_weather_status(input_string, dict_list):
    """
    converts status string into WeatherStatus enum,
    :param input_string: description string from REST-API
    :param dict_list: dictionary to compare input_string with.
    :return: key value from dict_list
    """
    if input_string is not None:
        for dictionary in dict_list:
            for key in dictionary:
                if key == input_string:
                    return dictionary[key]
    return None


def refresh():
    """
    calls REST-API and converts json into appropiate information for global variable
    'weekStatus'
    """
    try:
        data = call_api()
        decode_json(data)
    except Exception as e:
        wlogging.log(LogType.ERROR.value, LogMessage.ERR_API_CONN.name, LogMessage.ERR_API_CONN.value + ': ' + str(e))


refresh() # get data first time
# print("API1")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[1].rain)
