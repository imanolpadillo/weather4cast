# *************************************************************************************************** 
# ****************************************** WEATHER API2 *******************************************
# *************************************************************************************************** 
# Source: https://openweathermap.org/api

import requests
from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

DAYS = 5

class WeatherStatus(Enum):
    SUNNY = 1
    PARTLY_CLOUDY = 2
    CLOUDY = 3
    RAINY = 4
    STORMY = 5
    WINDY = 6
    FOGGY = 7
    SNOWY = 8
 
dict_weather_status = [
                       {'snow': WeatherStatus.SNOWY}, \
                       {'thunderstorm': WeatherStatus.STORMY}, \
                       {'clear': WeatherStatus.SUNNY}, \
                       {'drizzle': WeatherStatus.RAINY}, \
                       {'rain': WeatherStatus.RAINY}, \
                       {'fog': WeatherStatus.FOGGY}, \
                       {'clouds': WeatherStatus.CLOUDY}
                    ]

class DayWeather:
    def __init__(self, status=None, rain=None, temperature=None):
        self.status = status if status is not None else ["-"]*24
        self.rain = rain if rain is not None else ["0"]*24
        self.temperature = temperature if temperature is not None else ["-"]*24

weekWeather = [DayWeather() for _ in range(DAYS+1)]  

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def call_api():
    """
    calls REST-API from "el-tiempo.net"
    :return: json file
    """ 
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=42.8465088&lon=-2.6724025&units=metric&appid=0490c3ec80c848e85ddda40210bc5693'
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
    first_temperature = ''
    first_status = ''
    counter=0
    day_index=0
    for item in data['list']:
        if counter == 0:
            first_temperature = item['main']['temp']
            first_status = item['weather'][0]['main']
        if item['dt_txt'][11:13] == "00":
            weekWeather[day_index].temperature[0] = item['main']['temp']
            weekWeather[day_index].temperature[1] = item['main']['temp']
            weekWeather[day_index].temperature[2] = item['main']['temp']
            weekWeather[day_index].status[0] = item['weather'][0]['main']
            weekWeather[day_index].status[1] = item['weather'][0]['main']
            weekWeather[day_index].status[2] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[0] = item['rain']['3h']
                weekWeather[day_index].rain[1] = item['rain']['3h']
                weekWeather[day_index].rain[2] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "03":
            weekWeather[day_index].temperature[3] = item['main']['temp']
            weekWeather[day_index].temperature[4] = item['main']['temp']
            weekWeather[day_index].temperature[5] = item['main']['temp']
            weekWeather[day_index].status[3] = item['weather'][0]['main']
            weekWeather[day_index].status[4] = item['weather'][0]['main']
            weekWeather[day_index].status[5] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[3] = item['rain']['3h']
                weekWeather[day_index].rain[4] = item['rain']['3h']
                weekWeather[day_index].rain[5] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "06":
            weekWeather[day_index].temperature[6] = item['main']['temp']
            weekWeather[day_index].temperature[7] = item['main']['temp']
            weekWeather[day_index].temperature[8] = item['main']['temp']
            weekWeather[day_index].status[6] = item['weather'][0]['main']
            weekWeather[day_index].status[7] = item['weather'][0]['main']
            weekWeather[day_index].status[8] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[6] = item['rain']['3h']
                weekWeather[day_index].rain[7] = item['rain']['3h']
                weekWeather[day_index].rain[8] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "09":
            weekWeather[day_index].temperature[9] = item['main']['temp']
            weekWeather[day_index].temperature[10] = item['main']['temp']
            weekWeather[day_index].temperature[11] = item['main']['temp']
            weekWeather[day_index].status[9] = item['weather'][0]['main']
            weekWeather[day_index].status[10] = item['weather'][0]['main']
            weekWeather[day_index].status[11] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[9] = item['rain']['3h']
                weekWeather[day_index].rain[10] = item['rain']['3h']
                weekWeather[day_index].rain[11] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "12":
            weekWeather[day_index].temperature[12] = item['main']['temp']
            weekWeather[day_index].temperature[13] = item['main']['temp']
            weekWeather[day_index].temperature[14] = item['main']['temp']
            weekWeather[day_index].status[12] = item['weather'][0]['main']
            weekWeather[day_index].status[13] = item['weather'][0]['main']
            weekWeather[day_index].status[14] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[12] = item['rain']['3h']
                weekWeather[day_index].rain[13] = item['rain']['3h']
                weekWeather[day_index].rain[14] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "15":
            weekWeather[day_index].temperature[15] = item['main']['temp']
            weekWeather[day_index].temperature[16] = item['main']['temp']
            weekWeather[day_index].temperature[17] = item['main']['temp']
            weekWeather[day_index].status[15] = item['weather'][0]['main']
            weekWeather[day_index].status[16] = item['weather'][0]['main']
            weekWeather[day_index].status[17] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[15] = item['rain']['3h']
                weekWeather[day_index].rain[16] = item['rain']['3h']
                weekWeather[day_index].rain[17] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "18":
            weekWeather[day_index].temperature[18] = item['main']['temp']
            weekWeather[day_index].temperature[19] = item['main']['temp']
            weekWeather[day_index].temperature[20] = item['main']['temp']
            weekWeather[day_index].status[18] = item['weather'][0]['main']
            weekWeather[day_index].status[19] = item['weather'][0]['main']
            weekWeather[day_index].status[20] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[18] = item['rain']['3h']
                weekWeather[day_index].rain[19] = item['rain']['3h']
                weekWeather[day_index].rain[20] = item['rain']['3h']
        elif item['dt_txt'][11:13] == "21":
            weekWeather[day_index].temperature[21] = item['main']['temp']
            weekWeather[day_index].temperature[22] = item['main']['temp']
            weekWeather[day_index].temperature[23] = item['main']['temp']
            weekWeather[day_index].status[21] = item['weather'][0]['main']
            weekWeather[day_index].status[22] = item['weather'][0]['main']
            weekWeather[day_index].status[23] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[21] = item['rain']['3h']
                weekWeather[day_index].rain[22] = item['rain']['3h']
                weekWeather[day_index].rain[23] = item['rain']['3h']
            day_index+=1
        counter+=1

    # Replace empy temperature + status by first_perature and first_status
    for x in range(len(weekWeather)):
        for ycount, yvalue in enumerate(weekWeather[x].status):
            if weekWeather[x].status[ycount] == '-':
                weekWeather[x].status[ycount] = first_status
                weekWeather[x].temperature[ycount] = first_temperature

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
    for dictionary in dict_list:
        for key in dictionary:
            if key.lower() in input_string.lower():
                return dictionary[key]
    return None


def refresh():
    """
    calls REST-API and converts json into appropiate information for global variable
    'weekStatus'
    """
    data = call_api()
    decode_json(data)