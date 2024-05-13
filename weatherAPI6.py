# *************************************************************************************************** 
# ****************************************** WEATHER API6 *******************************************
# *************************************************************************************************** 
# Source: https://docs.meteoblue.com/en/weather-apis/packages-api/overview
# API renewal: https://www.meteoblue.com/en/weather-api/index/overview

import requests, math
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import configparser
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

config = configparser.ConfigParser()
config.read('secrets.ini')
api_key = config['secrets']['api6_key']
api_url =  'http://my.meteoblue.com/packagesV2/basic-1h?lat=42.85&lon=-2.6727&apikey=' + api_key
api_name = 'meteblue'
api_refresh_s = 1800

#pictocode: https://content.meteoblue.com/es/investigacion-educacion/especificaciones/standards/simbolos-y-pictogramas
dict_weather_status = [
                       {1: WeatherStatus.SUNNY}, \
                       {2: WeatherStatus.SUNNY}, \
                       {3: WeatherStatus.SUNNY}, \
                       {4: WeatherStatus.SUNNY}, \
                       {5: WeatherStatus.SUNNY}, \
                       {6: WeatherStatus.SUNNY}, \
                       {7: WeatherStatus.PARTLY_CLOUDY}, \
                       {8: WeatherStatus.PARTLY_CLOUDY}, \
                       {9: WeatherStatus.PARTLY_CLOUDY}, \
                       {10: WeatherStatus.STORMY}, \
                       {11: WeatherStatus.STORMY}, \
                       {12: WeatherStatus.STORMY}, \
                       {13: WeatherStatus.FOGGY}, \
                       {14: WeatherStatus.FOGGY}, \
                       {15: WeatherStatus.FOGGY}, \
                       {16: WeatherStatus.FOGGY}, \
                       {17: WeatherStatus.FOGGY}, \
                       {18: WeatherStatus.FOGGY}, \
                       {19: WeatherStatus.CLOUDY}, \
                       {20: WeatherStatus.CLOUDY}, \
                       {21: WeatherStatus.CLOUDY}, \
                       {22: WeatherStatus.CLOUDY}, \
                       {23: WeatherStatus.RAINY}, \
                       {24: WeatherStatus.SNOWY}, \
                       {25: WeatherStatus.RAINY}, \
                       {26: WeatherStatus.SNOWY}, \
                       {27: WeatherStatus.STORMY}, \
                       {28: WeatherStatus.STORMY}, \
                       {29: WeatherStatus.SNOWY}, \
                       {30: WeatherStatus.STORMY}, \
                       {31: WeatherStatus.RAINY}, \
                       {32: WeatherStatus.SNOWY}, \
                       {33: WeatherStatus.RAINY}, \
                       {34: WeatherStatus.FOGGY}, \
                       {35: WeatherStatus.SNOWY}, \
                       {100: WeatherStatus.WINDY}
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
            weekWeather[day].temperature[hour] = round(data['data_1h']['temperature'][count])
            weekWeather[day].rain[hour] = ceil_half(data['data_1h']['precipitation'][count])
            if (data['data_1h']['windspeed'][count]>WeatherConfig.MAX_WIND_MS.value):
                #wind status is not defined in 'weather code'
                weekWeather[day].status[hour] = 100 # windy code
            else:
                weekWeather[day].status[hour] = int(data['data_1h']['pictocode'][count])
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
# print("API6")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)
