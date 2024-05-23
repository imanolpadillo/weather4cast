# *************************************************************************************************** 
# ************************************* WEATHER API: METEMATI ***************************************
# *************************************************************************************************** 
# Source: https://www.meteomatics.com/en/api/getting-started/

import requests, math, os
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import configparser
import wlogging
from wlogging import LogType, LogMessage
from datetime import datetime, timedelta

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

def get_current_day (day_offset):
    """
    get current date + day offset in format 'YYYY-MM-DD'
    :param day_offset: day offset
    :return: date in format 'YYYY-MM-DD'
    """ 
    # Get the current date
    current_date = datetime.now()

    # Calculate the date for the day after tomorrow
    output_date = current_date + timedelta(days=day_offset)

    # Format the current date as YYYY-MM-DD
    return output_date.strftime("%Y-%m-%d")

init_date = get_current_day(0)
end_date = get_current_day(WeatherConfig.DAYS.value)

script_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file_path = os.path.join(script_dir, 'secrets.ini')
config = configparser.ConfigParser()
config.read(secrets_file_path)

api_name = 'metemati'
api_refresh_s = 900
api_key = config['secrets'][api_name]
#https://api.meteomatics.com/2024-05-12T00:00:00.000+02:00--2024-05-18T00:00:00.000+02:00:PT1H/t_2m:C,precip_1h:mm,weather_symbol_1h:idx,wind_speed_10m:ms/42.8465088,-2.6724025/json
api_url =  'https://personalproject_caseof_usein:' + api_key + \
    '@api.meteomatics.com/' + init_date + 'T00:00:00.000+02:00--' + end_date + \
    'T00:00:00.000+02:00:PT1H/t_2m:C,precip_1h:mm,weather_symbol_1h:idx,wind_speed_10m:ms/42.8465088,-2.6724025/json'

#weather symbol: https://www.meteomatics.com/en/api/available-parameters/weather-parameter/general-weather-state/
dict_weather_status = [
                       {1: WeatherStatus.SUNNY}, \
                       {101: WeatherStatus.SUNNY}, \
                       {2: WeatherStatus.SUNNY}, \
                       {102: WeatherStatus.SUNNY}, \
                       {3: WeatherStatus.PARTLY_CLOUDY}, \
                       {103: WeatherStatus.PARTLY_CLOUDY}, \
                       {4: WeatherStatus.CLOUDY}, \
                       {104: WeatherStatus.CLOUDY}, \
                       {5: WeatherStatus.RAINY}, \
                       {105: WeatherStatus.RAINY}, \
                       {6: WeatherStatus.SNOWY}, \
                       {106: WeatherStatus.SNOWY}, \
                       {7: WeatherStatus.SNOWY}, \
                       {107: WeatherStatus.SNOWY}, \
                       {8: WeatherStatus.RAINY}, \
                       {108: WeatherStatus.RAINY}, \
                       {9: WeatherStatus.SNOWY}, \
                       {109: WeatherStatus.SNOWY}, \
                       {10: WeatherStatus.RAINY}, \
                       {110: WeatherStatus.RAINY}, \
                       {11: WeatherStatus.FOGGY}, \
                       {111: WeatherStatus.FOGGY}, \
                       {12: WeatherStatus.FOGGY}, \
                       {112: WeatherStatus.FOGGY}, \
                       {13: WeatherStatus.RAINY}, \
                       {113: WeatherStatus.RAINY}, \
                       {14: WeatherStatus.STORMY}, \
                       {114: WeatherStatus.STORMY}, \
                       {15: WeatherStatus.RAINY}, \
                       {115: WeatherStatus.RAINY}, \
                       {16: WeatherStatus.STORMY}, \
                       {116: WeatherStatus.STORMY}, \
                       {0: WeatherStatus.WINDY}
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
            weekWeather[day].temperature[hour] = round(data['data'][0]['coordinates'][0]['dates'][count]['value'])
            weekWeather[day].rain[hour] = round(data['data'][1]['coordinates'][0]['dates'][count]['value'],1)
            if (data['data'][3]['coordinates'][0]['dates'][count]['value']>WeatherConfig.MAX_WIND_MS.value):
                #wind status is not defined in 'weather code'
                weekWeather[day].status[hour] = 0 # windy code
            else:
                weekWeather[day].status[hour] = int(data['data'][2]['coordinates'][0]['dates'][count]['value'])
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
# print("METEMATI")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)

