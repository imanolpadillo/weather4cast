# *************************************************************************************************** 
# ****************************************** WEATHER API8 *******************************************
# *************************************************************************************************** 
# Source: https://dev.meteostat.net/api/

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
api_key = config['secrets']['api8_key']
api_url = "https://meteostat.p.rapidapi.com/stations/hourly"
api_name = 'metestat'
api_refresh_s = 5400

#status: https://dev.meteostat.net/formats.html#weather-condition-codes
dict_weather_status = [
                       {1: WeatherStatus.SUNNY}, \
                       {2: WeatherStatus.SUNNY}, \
                       {3: WeatherStatus.PARTLY_CLOUDY}, \
                       {4: WeatherStatus.CLOUDY}, \
                       {5: WeatherStatus.FOGGY}, \
                       {6: WeatherStatus.FOGGY}, \
                       {7: WeatherStatus.RAINY}, \
                       {8: WeatherStatus.RAINY}, \
                       {9: WeatherStatus.RAINY}, \
                       {10: WeatherStatus.RAINY}, \
                       {11: WeatherStatus.RAINY}, \
                       {12: WeatherStatus.SNOWY}, \
                       {13: WeatherStatus.SNOWY}, \
                       {14: WeatherStatus.SNOWY}, \
                       {15: WeatherStatus.SNOWY}, \
                       {16: WeatherStatus.SNOWY}, \
                       {17: WeatherStatus.RAINY}, \
                       {18: WeatherStatus.RAINY}, \
                       {19: WeatherStatus.SNOWY}, \
                       {20: WeatherStatus.SNOWY}, \
                       {21: WeatherStatus.SNOWY}, \
                       {22: WeatherStatus.SNOWY}, \
                       {23: WeatherStatus.STORMY}, \
                       {24: WeatherStatus.STORMY}, \
                       {25: WeatherStatus.STORMY}, \
                       {26: WeatherStatus.STORMY}, \
                       {27: WeatherStatus.STORMY}, \
                       {100: WeatherStatus.WINDY}
                    ]

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  # today + tomorrow + next days

# *************************************************************************************************** 
# FUNCTIONS
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
    headers = {
        'X-Rapidapi-Key': api_key,
        'X-Rapidapi-Host': "meteostat.p.rapidapi.com"
        }
    querystring = {"station":"08080","start":get_current_day(0),"end":get_current_day(WeatherConfig.DAYS.value),"tz":"Europe/Berlin"}

    response = requests.get(url, headers=headers, params=querystring)
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
            weekWeather[day].temperature[hour] = round(data['data'][count]['temp'])
            if data['data'][count]['prcp'] is None:
                weekWeather[day].rain[hour] = 0.0
            else:
                weekWeather[day].rain[hour] = ceil_half(data['data'][count]['prcp'])
            if (data['data'][count]['wspd'] * 1000 / 3600 >WeatherConfig.MAX_WIND_MS.value):
                #wind status is not defined in 'weather code'
                weekWeather[day].status[hour] = 100 # windy code
            else:
                weekWeather[day].status[hour] = data['data'][count]['coco']
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
# print("API8")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)

