# *************************************************************************************************** 
# ************************************* WEATHER API: VISUCROS ***************************************
# *************************************************************************************************** 
# Source: https://weather.visualcrossing.com

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

api_name = 'visucros'
api_refresh_s = 900
api_key = config['secrets'][api_name]
api_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/vitoria-gasteiz?unitGroup=metric&include=hours&contentType=json&key=' + api_key 

#src: https://www.visualcrossing.com/resources/documentation/weather-api/defining-icon-set-in-the-weather-api/
dict_weather_status = [
                       {'snow': WeatherStatus.SNOWY}, \
                       {'snow-showers-day': WeatherStatus.SNOWY}, \
                       {'snow-showers-night': WeatherStatus.SNOWY}, \
                       {'rain': WeatherStatus.RAINY}, \
                       {'fog': WeatherStatus.FOGGY}, \
                       {'wind': WeatherStatus.WINDY}, \
                       {'cloudy': WeatherStatus.CLOUDY}, \
                       {'partly-cloudy-day': WeatherStatus.PARTLY_CLOUDY}, \
                       {'partly-cloudy-night': WeatherStatus.PARTLY_CLOUDY}, \
                       {'clear-day': WeatherStatus.SUNNY}, \
                       {'clear-night': WeatherStatus.SUNNY}, \
                       {'thunder-rain': WeatherStatus.STORMY}, \
                       {'thunder-showers-day': WeatherStatus.STORMY}, \
                       {'thunder-showers-night': WeatherStatus.STORMY}, \
                       {'showers-day': WeatherStatus.RAINY}, \
                       {'showers-night': WeatherStatus.RAINY}
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
    for day in range(WeatherConfig.DAYS.value):
        for hour in range(24):
            weekWeather[day].temperature[hour] = round(data['days'][day]['hours'][hour]['temp'])
            weekWeather[day].rain[hour] = ceil_half(data['days'][day]['hours'][hour]['precip'])
            weekWeather[day].status[hour] = data['days'][day]['hours'][hour]['icon']
   
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
# print("API3")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)
