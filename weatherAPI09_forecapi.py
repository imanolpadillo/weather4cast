# *************************************************************************************************** 
# ************************************* WEATHER API: FORECAPI ***************************************
# *************************************************************************************************** 
# Source: https://rapidapi.com/foreca-ltd-foreca-ltd-default/api/foreca-weather
# Location: 103104499

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

api_name = 'forecapi'
api_refresh_s = 1800
api_key = config['secrets'][api_name]
api_url = "https://foreca-weather.p.rapidapi.com/forecast/hourly/103104499"
#status: https://developer.foreca.com/resources
dict_weather_status = [
                       {'000': WeatherStatus.SUNNY}, \
                       {'100': WeatherStatus.SUNNY}, \
                       {'200': WeatherStatus.PARTLY_CLOUDY}, \
                       {'300': WeatherStatus.PARTLY_CLOUDY}, \
                       {'400': WeatherStatus.CLOUDY}, \
                       {'500': WeatherStatus.FOGGY}, \
                       {'600': WeatherStatus.FOGGY}, \
                       {'210': WeatherStatus.RAINY}, \
                       {'310': WeatherStatus.RAINY}, \
                       {'410': WeatherStatus.RAINY}, \
                       {'220': WeatherStatus.RAINY}, \
                       {'320': WeatherStatus.RAINY}, \
                       {'420': WeatherStatus.RAINY}, \
                       {'430': WeatherStatus.RAINY}, \
                       {'240': WeatherStatus.STORMY}, \
                       {'340': WeatherStatus.STORMY}, \
                       {'440': WeatherStatus.STORMY}, \
                       {'211': WeatherStatus.SNOWY}, \
                       {'311': WeatherStatus.SNOWY}, \
                       {'411': WeatherStatus.SNOWY}, \
                       {'221': WeatherStatus.SNOWY}, \
                       {'321': WeatherStatus.SNOWY}, \
                       {'421': WeatherStatus.SNOWY}, \
                       {'431': WeatherStatus.SNOWY}, \
                       {'212': WeatherStatus.SNOWY}, \
                       {'312': WeatherStatus.SNOWY}, \
                       {'412': WeatherStatus.SNOWY}, \
                       {'222': WeatherStatus.SNOWY}, \
                       {'322': WeatherStatus.SNOWY}, \
                       {'422': WeatherStatus.SNOWY}, \
                       {'432': WeatherStatus.SNOWY}, \
                       {'999': WeatherStatus.WINDY}
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

def remove_yesterday_values(arr, split_date):
    for i, item in enumerate(arr):
        if split_date in item['time']:
            return arr[i:]
    return arr

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
        'X-Rapidapi-Host': "foreca-weather.p.rapidapi.com"
        }
    querystring = {"alt":"0","tempunit":"C","windunit":"MS","tz":"Europe/Madrid","periods":"168","dataset":"standard","history":"true"}

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

    # get date from today
    current_day = get_current_day(0)

    # delete elements before current day at 00:00
    data=remove_yesterday_values(data['forecast'], current_day + 'T00:00')
    print(data)

    count = 0
    for day in range(WeatherConfig.DAYS.value):
        for hour in range(24):
            weekWeather[day].temperature[hour] = round(data[count]['temperature'])
            weekWeather[day].rain[hour] = ceil_half(data[count]['precipAccum'])
            if (data[count]['windSpeed'] >WeatherConfig.MAX_WIND_MS.value):
                #wind status is not defined in 'weather code'
                weekWeather[day].status[hour] = 999 # windy code
            else:
                weekWeather[day].status[hour] = data[count]['symbol']
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
                if key in input_string:
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
print("API9")
print(weekWeather[0].temperature)
print(weekWeather[0].status)
print(weekWeather[0].rain)

