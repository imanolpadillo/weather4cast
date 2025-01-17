# *************************************************************************************************** 
# ************************************* WEATHER API: OWEATMAP ***************************************
# *************************************************************************************************** 
# Source: https://openweathermap.org/api

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

api_name = 'oweatmap'
api_refresh_s = 900
api_key = config['secrets'][api_name]
api_url =  'https://api.openweathermap.org/data/2.5/forecast?lat=' + WeatherConfig.GEO_LAT.value + \
'&lon=' + WeatherConfig.GEO_LON.value + '&units=metric&appid=' + api_key

dict_weather_status = [
                       {'snow': WeatherStatus.SNOWY}, \
                       {'thunderstorm': WeatherStatus.STORMY}, \
                       {'clear': WeatherStatus.SUNNY}, \
                       {'drizzle': WeatherStatus.RAINY}, \
                       {'rain': WeatherStatus.RAINY}, \
                       {'fog': WeatherStatus.FOGGY}, \
                       {'clouds': WeatherStatus.CLOUDY}
                    ]

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value+1)]  

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

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
    first_temperature = ''
    first_status = ''
    last_temperature = ''
    last_status = ''
    counter=0
    day_index=0
    for item in data['list']:
        if counter == 0:
            first_temperature = round(item['main']['temp'])
            first_status = item['weather'][0]['main']
        else:
            last_temperature = round(item['main']['temp'])
            last_status = item['weather'][0]['main']
        if item['dt_txt'][11:13] == "00":
            weekWeather[day_index].temperature[0] = round(item['main']['temp'])
            weekWeather[day_index].temperature[1] = round(item['main']['temp'])
            weekWeather[day_index].temperature[2] = round(item['main']['temp'])
            weekWeather[day_index].status[0] = item['weather'][0]['main']
            weekWeather[day_index].status[1] = item['weather'][0]['main']
            weekWeather[day_index].status[2] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[0] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[1] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[2] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "03":
            weekWeather[day_index].temperature[3] = round(item['main']['temp'])
            weekWeather[day_index].temperature[4] = round(item['main']['temp'])
            weekWeather[day_index].temperature[5] = round(item['main']['temp'])
            weekWeather[day_index].status[3] = item['weather'][0]['main']
            weekWeather[day_index].status[4] = item['weather'][0]['main']
            weekWeather[day_index].status[5] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[3] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[4] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[5] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "06":
            weekWeather[day_index].temperature[6] = round(item['main']['temp'])
            weekWeather[day_index].temperature[7] = round(item['main']['temp'])
            weekWeather[day_index].temperature[8] = round(item['main']['temp'])
            weekWeather[day_index].status[6] = item['weather'][0]['main']
            weekWeather[day_index].status[7] = item['weather'][0]['main']
            weekWeather[day_index].status[8] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[6] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[7] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[8] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "09":
            weekWeather[day_index].temperature[9] = round(item['main']['temp'])
            weekWeather[day_index].temperature[10] = round(item['main']['temp'])
            weekWeather[day_index].temperature[11] = round(item['main']['temp'])
            weekWeather[day_index].status[9] = item['weather'][0]['main']
            weekWeather[day_index].status[10] = item['weather'][0]['main']
            weekWeather[day_index].status[11] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[9] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[10] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[11] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "12":
            weekWeather[day_index].temperature[12] = round(item['main']['temp'])
            weekWeather[day_index].temperature[13] = round(item['main']['temp'])
            weekWeather[day_index].temperature[14] = round(item['main']['temp'])
            weekWeather[day_index].status[12] = item['weather'][0]['main']
            weekWeather[day_index].status[13] = item['weather'][0]['main']
            weekWeather[day_index].status[14] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[12] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[13] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[14] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "15":
            weekWeather[day_index].temperature[15] = round(item['main']['temp'])
            weekWeather[day_index].temperature[16] = round(item['main']['temp'])
            weekWeather[day_index].temperature[17] = round(item['main']['temp'])
            weekWeather[day_index].status[15] = item['weather'][0]['main']
            weekWeather[day_index].status[16] = item['weather'][0]['main']
            weekWeather[day_index].status[17] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[15] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[16] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[17] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "18":
            weekWeather[day_index].temperature[18] = round(item['main']['temp'])
            weekWeather[day_index].temperature[19] = round(item['main']['temp'])
            weekWeather[day_index].temperature[20] = round(item['main']['temp'])
            weekWeather[day_index].status[18] = item['weather'][0]['main']
            weekWeather[day_index].status[19] = item['weather'][0]['main']
            weekWeather[day_index].status[20] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[18] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[19] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[20] = round(item['rain']['3h'],1)
        elif item['dt_txt'][11:13] == "21":
            weekWeather[day_index].temperature[21] = round(item['main']['temp'])
            weekWeather[day_index].temperature[22] = round(item['main']['temp'])
            weekWeather[day_index].temperature[23] = round(item['main']['temp'])
            weekWeather[day_index].status[21] = item['weather'][0]['main']
            weekWeather[day_index].status[22] = item['weather'][0]['main']
            weekWeather[day_index].status[23] = item['weather'][0]['main']
            if 'rain' in item:
                weekWeather[day_index].rain[21] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[22] = round(item['rain']['3h'],1)
                weekWeather[day_index].rain[23] = round(item['rain']['3h'],1)
            day_index+=1
        counter+=1

    # Replace empty temperature + status by first_temperature and first_status
    for ycount, yvalue in enumerate(weekWeather[0].status):
        if weekWeather[0].status[ycount] is None:
            weekWeather[0].status[ycount] = first_status
            weekWeather[0].temperature[ycount] = first_temperature

    # Replace empty temperature + rain + status by last_temperature, last_status and last_rain
    for day in range(WeatherConfig.DAYS.value):
        for ycount, yvalue in enumerate(weekWeather[0].status):
            if weekWeather[day].status[ycount] is None:
                weekWeather[day].status[ycount] = last_status
                weekWeather[day].temperature[ycount] = last_temperature

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
                if key.lower() in input_string.lower():
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
# print("OWEATMAP")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)