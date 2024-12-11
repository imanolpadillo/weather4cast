# *************************************************************************************************** 
# ************************************* WEATHER API: 7TIMER   ***************************************
# *************************************************************************************************** 
# Source: https://github.com/Yeqzids/7timer-issues/wiki/Wiki

import requests, math
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
 
api_name = '7timer'
api_refresh_s = 900
api_url = 'https://www.7timer.info/bin/civil.php?lon=-2.6724025&lat=42.8465088&ac=0&unit=metric&output=json&tzshift=0'

dict_weather_status = [
                       {'clearday': WeatherStatus.SUNNY}, \
                       {'clearnight': WeatherStatus.SUNNY}, \
                       {'pcloudyday': WeatherStatus.PARTLY_CLOUDY}, \
                       {'pcloudynight': WeatherStatus.PARTLY_CLOUDY}, \
                       {'mcloudyday': WeatherStatus.PARTLY_CLOUDY}, \
                       {'mcloudynight': WeatherStatus.PARTLY_CLOUDY}, \
                       {'cloudyday': WeatherStatus.CLOUDY}, \
                       {'cloudynight': WeatherStatus.CLOUDY}, \
                       {'lightrainday': WeatherStatus.RAINY}, \
                       {'lightrainnight': WeatherStatus.RAINY}, \
                       {'oshowerday': WeatherStatus.RAINY}, \
                       {'oshowernight': WeatherStatus.RAINY}, \
                       {'ishowerday': WeatherStatus.RAINY}, \
                       {'ishowernight': WeatherStatus.RAINY}, \
                       {'rainday': WeatherStatus.RAINY}, \
                       {'rainnight': WeatherStatus.RAINY}, \
                       {'humidday': WeatherStatus.FOGGY}, \
                       {'humidnight': WeatherStatus.FOGGY}, \
                       {'lightsnowday': WeatherStatus.SNOWY}, \
                       {'lightsnownight': WeatherStatus.SNOWY}, \
                       {'rainsnowday': WeatherStatus.SNOWY}, \
                       {'rainsnownight': WeatherStatus.SNOWY}, \
                       {'tsday': WeatherStatus.STORMY}, \
                       {'tsnight': WeatherStatus.STORMY}, \
                       {'tsrainday': WeatherStatus.STORMY}, \
                       {'tsrainnight': WeatherStatus.STORMY}, \
                       {'windy': WeatherStatus.WINDY}
                    ]

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  # today + tomorrow + next days

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
    
def call_api():
    """
    calls REST-API from "7timer"
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
    calls REST-API from "7timer". Global variable "weekWeather" is updated.
    :param data: json file obtained from "7timer" REST-API
    :return: -
    """ 
    global weekWeather
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  

    temperature_array=[]
    status_array=[]
    rain_array=[]
    init_hour = int(data['init'][-2:]) + 1 # Madrid GMT+1
    
    # set data for hours from day 0 not included in api data
    for i in range(init_hour):
        temperature_array.append(data['dataseries'][0]['temp2m'])
        if data['dataseries'][0]['wind10m']['speed'] > WeatherConfig.MAX_WIND_MS.value:
            status_array.append('windy')
        else:
            status_array.append(data['dataseries'][0]['weather'])
        rain_array.append(data['dataseries'][0]['prec_amount'])        
    # set info from api (3hour slots)
    for item in data['dataseries']:
        for i in range(3):
            temperature_array.append(item['temp2m'])
            if item['wind10m']['speed'] > WeatherConfig.MAX_WIND_MS.value:
                status_array.append('windy')
            else:
                status_array.append(item['weather'])
            rain_array.append(item['prec_amount'])
            
    counter=0
    for day in range(5):
        for hour in range(24):
            weekWeather[day].temperature[hour] = temperature_array[counter]
            weekWeather[day].status[hour] = status_array [counter]
            weekWeather[day].rain[hour] = rain_array[counter]
            counter+=1

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

#refresh() # get data first time
#print("7TIMER")
#print(weekWeather[0].temperature)
#print(weekWeather[0].status)
#print(weekWeather[0].rain)
