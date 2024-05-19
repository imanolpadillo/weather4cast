# *************************************************************************************************** 
# ************************************* WEATHER API: TOMORROW ***************************************
# *************************************************************************************************** 
# Source: https://docs.tomorrow.io/

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

api_name = 'tomorrow'
api_refresh_s = 900
api_key = config['secrets'][api_name]
api_url =  'https://api.tomorrow.io/v4/timelines?location=42.8597,-2.6818&fields=temperature,weatherCode,precipitationIntensity,windSpeed&units=metric&timesteps=1h&apikey=' + api_key

# Source: https://docs.tomorrow.io/reference/data-layers-weather-codes
dict_weather_status = [
                       {1000:  WeatherStatus.SUNNY}, \
                       {1100:  WeatherStatus.SUNNY}, \
                       {1101:  WeatherStatus.PARTLY_CLOUDY}, \
                       {1102:  WeatherStatus.PARTLY_CLOUDY}, \
                       {1001:  WeatherStatus.CLOUDY}, \
                       {2000:  WeatherStatus.FOGGY}, \
                       {2100:  WeatherStatus.FOGGY}, \
                       {4000:  WeatherStatus.RAINY}, \
                       {4001:  WeatherStatus.RAINY}, \
                       {4200:  WeatherStatus.RAINY}, \
                       {4201:  WeatherStatus.RAINY}, \
                       {5000:  WeatherStatus.SNOWY}, \
                       {5001:  WeatherStatus.SNOWY}, \
                       {5100:  WeatherStatus.SNOWY}, \
                       {5101:  WeatherStatus.SNOWY}, \
                       {6000:  WeatherStatus.RAINY}, \
                       {6001:  WeatherStatus.RAINY}, \
                       {6200:  WeatherStatus.RAINY}, \
                       {6201:  WeatherStatus.RAINY}, \
                       {7000:  WeatherStatus.RAINY}, \
                       {7101:  WeatherStatus.RAINY}, \
                       {7102:  WeatherStatus.RAINY}, \
                       {8000:  WeatherStatus.STORMY},
                       {9999:  WeatherStatus.WINDY}
                    ]

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value+1)]  

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def round_half(value):
    # Calculate the integer part of the number
    integer_part = int(value)
    # Calculate the fractional part of the number
    fractional_part = value - integer_part
    # Determine the rounding
    if fractional_part < 0.25:
        rounded_value = integer_part
    elif fractional_part < 0.75:
        rounded_value = integer_part + 0.5
    else:
        rounded_value = integer_part + 1.0
    return rounded_value

def call_api():
    """
    calls REST-API from "el-tiempo.net"
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
    calls REST-API from "openweathermap". Global variable "weekWeather" is updated.
    :param data: json file obtained from "openweathermap" REST-API
    :return: -
    """ 
    global weekWeather
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  
    first_temperature = 0
    first_status = 0
    first_rain = 0
    counter=0
    day_index=0
    for item in data['data']['timelines'][0]['intervals']:
        if counter == 0:
            first_temperature = round(item['values']['temperature'])
            first_status = int(item['values']['weatherCode'])
            first_rain = round_half(round(float(item['values']['precipitationIntensity']), 1))
        hour = int(item['startTime'][11:13])
        weekWeather[day_index].temperature[hour] = round(item['values']['temperature'])
        if int(item['values']['windSpeed']) > WeatherConfig.MAX_WIND_MS.value:
            weekWeather[day_index].status[hour] = 9999  #windy
        else:
            weekWeather[day_index].status[hour] = int(item['values']['weatherCode'])
        weekWeather[day_index].rain[hour] = round_half(round(float(item['values']['precipitationIntensity']), 1))
        counter+=1
        if hour == 23:
            day_index+=1

    # Replace empy temperature + rain + status by first_temperature, first_status and first_rain
    for ycount, yvalue in enumerate(weekWeather[0].status):
        if weekWeather[0].status[ycount] is None:
            weekWeather[0].status[ycount] = first_status
            weekWeather[0].temperature[ycount] = first_temperature
            weekWeather[0].rain[ycount] = first_rain
            

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
        return

# refresh() # get data first time
# print("TOMORROW")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)