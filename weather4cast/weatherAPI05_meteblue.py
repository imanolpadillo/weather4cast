# *************************************************************************************************** 
# ************************************* WEATHER API: METEBLUE ***************************************
# *************************************************************************************************** 
# Source: https://docs.meteoblue.com/en/weather-apis/packages-api/overview
# API renewal: https://www.meteoblue.com/en/weather-api/index/overview

import requests, math, os
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import configparser
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
script_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file_path = os.path.join(script_dir, 'secrets.ini')
config = configparser.ConfigParser()
config.read(secrets_file_path)

api_name = 'meteblue'
api_refresh_s = 28800
api_key = config['secrets'][api_name]
api_url =  'http://my.meteoblue.com/packagesV2/basic-1h?lat=' + WeatherConfig.GEO_LAT.value + \
'&lon=' + WeatherConfig.GEO_LON.value + '&apikey=' + api_key

#pictocode: https://content.meteoblue.com/es/investigacion-educacion/especificaciones/standards/simbolos-y-pictogramas
dict_weather_status = [
                       {1: WeatherStatus.SUNNY}, \
                       {2: WeatherStatus.SUNNY}, \
                       {3: WeatherStatus.SUNNY}, \
                       {4: WeatherStatus.FOGGY}, \
                       {5: WeatherStatus.FOGGY}, \
                       {6: WeatherStatus.FOGGY}, \
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
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  
    count = 0
    for day in range(WeatherConfig.DAYS.value):
        for hour in range(24):
            weekWeather[day].temperature[hour] = round(data['data_1h']['temperature'][count])
            weekWeather[day].rain[hour] = round(data['data_1h']['precipitation'][count],1)
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


# refresh() # get data first time
# print("METEBLUE")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)
