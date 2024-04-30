# *************************************************************************************************** 
# ****************************************** WEATHER API3 *******************************************
# *************************************************************************************************** 
# Source: https://docs.tomorrow.io/

import requests, math
from weatherAPIenum import WeatherStatus, DAYS, DayWeather
import configparser
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

config = configparser.ConfigParser()
config.read('secrets.ini')
api_key = config['secrets']['api3_key']
api_url =  'https://api.tomorrow.io/v4/timelines?location=42.8597,-2.6818&fields=temperature,weatherCode,precipitationIntensity,windSpeed&units=metric&timesteps=1h&apikey=' + api_key

WIND_MAX_MS = 12

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

weekWeather = [DayWeather() for _ in range(DAYS+1)]  

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
    first_temperature = 0
    first_status = 0
    first_rain = 0
    counter=0
    day_index=0
    for item in data['data']['timelines'][0]['intervals']:
        if counter == 0:
            first_temperature = round(item['values']['temperature'])
            first_status = int(item['values']['weatherCode'])
            first_rain = ceil_half(item['values']['precipitationIntensity'])
        hour = int(item['startTime'][11:13])
        weekWeather[day_index].temperature[hour] = round(item['values']['temperature'])
        if int(item['values']['windSpeed']) > WIND_MAX_MS:
            weekWeather[day_index].status[hour] = 9999  #windy
        else:
            weekWeather[day_index].status[hour] = int(item['values']['weatherCode'])
        weekWeather[day_index].rain[hour] = ceil_half(item['values']['precipitationIntensity'])
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

refresh() # get data first time
# print("API3")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)