# ***************************************************************************************************
# ************************************* WEATHER API: AIWEATHR ***************************************
# ***************************************************************************************************
# Source: https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/
 
import requests,math
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import configparser
import wlogging
from wlogging import LogType, LogMessage
from datetime import datetime, timedelta
 
# ***************************************************************************************************
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
config = configparser.ConfigParser()
config.read('secrets.ini')
 
api_name = 'aiweathr'
api_refresh_s = 28800
api_key = config['secrets'][api_name]
api_url = 'https://ai-weather-by-meteosource.p.rapidapi.com/hourly'
#status: https://www.meteosource.com/documentation#point
dict_weather_status = [
                       {2: WeatherStatus.SUNNY}, \
                       {3: WeatherStatus.SUNNY}, \
                       {4: WeatherStatus.PARTLY_CLOUDY}, \
                       {5: WeatherStatus.PARTLY_CLOUDY}, \
                       {6: WeatherStatus.CLOUDY}, \
                       {7: WeatherStatus.CLOUDY}, \
                       {8: WeatherStatus.CLOUDY}, \
                       {9: WeatherStatus.FOGGY}, \
                       {10: WeatherStatus.RAINY}, \
                       {11: WeatherStatus.RAINY}, \
                       {12: WeatherStatus.RAINY}, \
                       {13: WeatherStatus.RAINY}, \
                       {14: WeatherStatus.STORMY}, \
                       {15: WeatherStatus.STORMY}, \
                       {16: WeatherStatus.SNOWY}, \
                       {17: WeatherStatus.SNOWY}, \
                       {18: WeatherStatus.SNOWY}, \
                       {19: WeatherStatus.SNOWY}, \
                       {20: WeatherStatus.SNOWY}, \
                       {21: WeatherStatus.SNOWY}, \
                       {22: WeatherStatus.SNOWY}, \
                       {23: WeatherStatus.RAINY}, \
                       {24: WeatherStatus.RAINY}, \
                       {25: WeatherStatus.RAINY}, \
                       {26: WeatherStatus.SUNNY}, \
                       {27: WeatherStatus.SUNNY}, \
                       {28: WeatherStatus.PARTLY_CLOUDY}, \
                       {29: WeatherStatus.PARTLY_CLOUDY}, \
                       {30: WeatherStatus.CLOUDY}, \
                       {31: WeatherStatus.CLOUDY}, \
                       {32: WeatherStatus.RAINY}, \
                       {33: WeatherStatus.STORMY}, \
                       {34: WeatherStatus.SNOWY}, \
                       {35: WeatherStatus.SNOWY}, \
                       {36: WeatherStatus.RAINY}
                    ]
 
weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  # today + tomorrow + next days
 
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
    calls REST-API
    :return: json file
    """
    url = api_url
    headers = {
        'X-Rapidapi-Key': api_key,
        'X-Rapidapi-Host': "ai-weather-by-meteosource.p.rapidapi.com"
        }
    querystring = {"place_id":"gasteiz-vitoria","timezone":"auto","language":"en","units":"metric"}
 
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None
 
def decode_json(data):
    """
    REST-API response is decoded. Global variable "weekWeather" is updated.
    :param data: json file obtained from "el-tiempo.net" REST-API
    :return: -
    """
    global weekWeather
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value+1)]  
 
    # This API gets 120 values (5days) from current hour. That means that previous hours from today
    # must be set to current value, and next hours from today + 5 days must be set to value of
    # current hour in 5 days.
    # get first given hour and last index
    first_hour = int(datetime.fromisoformat(data['hourly']['data'][0]['date']).hour)
    last_index = len(data['hourly']['data'])
 
    count = 0
    for day in range(WeatherConfig.DAYS.value):
        for hour in range(24):
            # set values of first given hour to dayly previous values
            if count<=first_hour:
                index = 0
                index_offset = count
            elif count>=last_index:
                index=last_index-1
            else:
                index = count - index_offset
            weekWeather[day].temperature[hour] = round(data['hourly']['data'][index]['temperature'])
            weekWeather[day].rain[hour] = ceil_half(data['hourly']['data'][index]['precipitation']['total'])
            if (data['hourly']['data'][index]['wind']['speed'] >WeatherConfig.MAX_WIND_MS.value):
                #wind status is not defined in 'weather code'
                weekWeather[day].status[hour] = 100 # windy code
            else:
                weekWeather[day].status[hour] = data['hourly']['data'][index]['icon']
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
        print(data)
        decode_json(data)
    except Exception as e:
        wlogging.log(LogType.ERROR.value, LogMessage.ERR_API_CONN.name, LogMessage.ERR_API_CONN.value + ': ' + str(e))
 

refresh() # get data first time
print("API10")
print(weekWeather[0].temperature)
print(weekWeather[0].status)
print(weekWeather[0].rain)
 
 