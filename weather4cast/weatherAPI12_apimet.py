# *************************************************************************************************** 
# ************************************* WEATHER API: APIMET   ***************************************
# *************************************************************************************************** 
# Source: https://api.met.no/weatherapi/locationforecast/2.0/documentation

import requests, math
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import wlogging
from wlogging import LogType, LogMessage
from datetime import datetime

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
 
api_name = 'apimet'
api_refresh_s = 900
api_url = 'https://api.met.no/weatherapi/locationforecast/2.0?lat=42.8465088&lon=-2.6724025&altitude=525'

dict_weather_status = [
    {'clearsky_day': WeatherStatus.SUNNY},
    {'clearsky_night': WeatherStatus.SUNNY},
    {'clearsky_polartwilight': WeatherStatus.SUNNY},
    {'fair_day': WeatherStatus.SUNNY},
    {'fair_night': WeatherStatus.SUNNY},
    {'fair_polartwilight': WeatherStatus.SUNNY},
    {'partlycloudy_day': WeatherStatus.PARTLY_CLOUDY},
    {'partlycloudy_night': WeatherStatus.PARTLY_CLOUDY},
    {'partlycloudy_polartwilight': WeatherStatus.PARTLY_CLOUDY},
    {'cloudy': WeatherStatus.CLOUDY},
    {'rainshowers_day': WeatherStatus.RAINY},
    {'rainshowers_night': WeatherStatus.RAINY},
    {'rainshowers_polartwilight': WeatherStatus.RAINY},
    {'rainshowersandthunder_day': WeatherStatus.STORMY},
    {'rainshowersandthunder_night': WeatherStatus.STORMY},
    {'rainshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'sleetshowers_day': WeatherStatus.SNOWY},
    {'sleetshowers_night': WeatherStatus.SNOWY},
    {'sleetshowers_polartwilight': WeatherStatus.SNOWY},
    {'snowshowers_day': WeatherStatus.SNOWY},
    {'snowshowers_night': WeatherStatus.SNOWY},
    {'snowshowers_polartwilight': WeatherStatus.SNOWY},
    {'rain': WeatherStatus.RAINY},
    {'heavyrain': WeatherStatus.RAINY},
    {'heavyrainandthunder': WeatherStatus.STORMY},
    {'sleet': WeatherStatus.SNOWY},
    {'snow': WeatherStatus.SNOWY},
    {'snowandthunder': WeatherStatus.STORMY},
    {'fog': WeatherStatus.FOGGY},
    {'sleetshowersandthunder_day': WeatherStatus.STORMY},
    {'sleetshowersandthunder_night': WeatherStatus.STORMY},
    {'sleetshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'snowshowersandthunder_day': WeatherStatus.STORMY},
    {'snowshowersandthunder_night': WeatherStatus.STORMY},
    {'snowshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'rainandthunder': WeatherStatus.STORMY},
    {'sleetandthunder': WeatherStatus.STORMY},
    {'lightrainshowersandthunder_day': WeatherStatus.STORMY},
    {'lightrainshowersandthunder_night': WeatherStatus.STORMY},
    {'lightrainshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'heavyrainshowersandthunder_day': WeatherStatus.STORMY},
    {'heavyrainshowersandthunder_night': WeatherStatus.STORMY},
    {'heavyrainshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'lightssleetshowersandthunder_day': WeatherStatus.STORMY},
    {'lightssleetshowersandthunder_night': WeatherStatus.STORMY},
    {'lightssleetshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'heavysleetshowersandthunder_day': WeatherStatus.STORMY},
    {'heavysleetshowersandthunder_night': WeatherStatus.STORMY},
    {'heavysleetshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'lightssnowshowersandthunder_day': WeatherStatus.STORMY},
    {'lightssnowshowersandthunder_night': WeatherStatus.STORMY},
    {'lightssnowshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'heavysnowshowersandthunder_day': WeatherStatus.STORMY},
    {'heavysnowshowersandthunder_night': WeatherStatus.STORMY},
    {'heavysnowshowersandthunder_polartwilight': WeatherStatus.STORMY},
    {'lightrainandthunder': WeatherStatus.STORMY},
    {'lightsleetandthunder': WeatherStatus.STORMY},
    {'heavysleetandthunder': WeatherStatus.STORMY},
    {'lightsnowandthunder': WeatherStatus.STORMY},
    {'heavysnowandthunder': WeatherStatus.STORMY},
    {'lightrainshowers_day': WeatherStatus.RAINY},
    {'lightrainshowers_night': WeatherStatus.RAINY},
    {'lightrainshowers_polartwilight': WeatherStatus.RAINY},
    {'heavyrainshowers_day': WeatherStatus.RAINY},
    {'heavyrainshowers_night': WeatherStatus.RAINY},
    {'heavyrainshowers_polartwilight': WeatherStatus.RAINY},
    {'lightsleetshowers_day': WeatherStatus.SNOWY},
    {'lightsleetshowers_night': WeatherStatus.SNOWY},
    {'lightsleetshowers_polartwilight': WeatherStatus.SNOWY},
    {'heavysleetshowers_day': WeatherStatus.SNOWY},
    {'heavysleetshowers_night': WeatherStatus.SNOWY},
    {'heavysleetshowers_polartwilight': WeatherStatus.SNOWY},
    {'lightsnowshowers_day': WeatherStatus.SNOWY},
    {'lightsnowshowers_night': WeatherStatus.SNOWY},
    {'lightsnowshowers_polartwilight': WeatherStatus.SNOWY},
    {'heavysnowshowers_day': WeatherStatus.SNOWY},
    {'heavysnowshowers_night': WeatherStatus.SNOWY},
    {'heavysnowshowers_polartwilight': WeatherStatus.SNOWY},
    {'lightrain': WeatherStatus.RAINY},
    {'lightsleet': WeatherStatus.SNOWY},
    {'heavysleet': WeatherStatus.SNOWY},
    {'lightsnow': WeatherStatus.SNOWY},
    {'heavysnow': WeatherStatus.SNOWY},
    {'windy': WeatherStatus.WINDY},
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
    # Define headers (User-Agent is required for this API)
    headers = {
        "User-Agent": "YourAppName/1.0 (your_email@example.com)"  # Replace with your app name and email
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def decode_json(data):
    """
    calls REST-API from "apimet". Global variable "weekWeather" is updated.
    :param data: json file obtained from "apimet" REST-API
    :return: -
    """ 
    global weekWeather
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  

    last_time = -1
    temperature_array=[]
    status_array=[]
    rain_array=[]
    init_hour = datetime.strptime((data['properties']['timeseries'][0]['time']), "%Y-%m-%dT%H:%M:%SZ").hour
    
    # set data for hours from day 0 not included in api data
    for i in range(init_hour):
        temperature_array.append(data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature'])
        if data['properties']['timeseries'][0]['data']['instant']['details']['wind_speed'] > WeatherConfig.MAX_WIND_MS.value:
            status_array.append('windy')
        else:
            status_array.append(data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code'])
        rain_array.append(data['properties']['timeseries'][0]['data']['next_1_hours']['details']['precipitation_amount'])        
    # set info from api
    for item in data['properties']['timeseries']:
        if "next_1_hours" in item['data'] or "next_6_hours" in item['data'] or "next_12_hours" in item['data'] :

            current_time = int(datetime.strptime((item['time']), "%Y-%m-%dT%H:%M:%SZ").hour)
            if  not(current_time == 0 and last_time==23) and last_time != -1 and (current_time - last_time) != 1:
                if current_time == 0:
                    current_time = 24
                for i in range (abs(current_time - last_time) -1):
                    temperature_array.append(temperature_array[-1])
                    status_array.append(status_array[-1])
                    rain_array.append(rain_array[-1])

            temperature_array.append(item['data']['instant']['details']['air_temperature'])
            if item['data']['instant']['details']['wind_speed'] > WeatherConfig.MAX_WIND_MS.value:
                status_array.append('windy')
            else:
                try:
                    status_array.append(item['data']['next_1_hours']['summary']['symbol_code'])
                except:
                    try:
                        status_array.append(item['data']['next_6_hours']['summary']['symbol_code'])
                    except:
                        status_array.append(item['data']['next_12_hours']['summary']['symbol_code'])
            try:
                rain_array.append(item['data']['next_1_hours']['details']['precipitation_amount'])
            except:
                try:
                    rain_array.append(item['data']['next_6_hours']['details']['precipitation_amount'])
                except:
                    rain_array.append(item['data']['next_12_hours']['details']['precipitation_amount'])
            last_time = int(datetime.strptime((item['time']), "%Y-%m-%dT%H:%M:%SZ").hour)
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
#print("apimet")
#print(weekWeather[0].temperature)
#print(weekWeather[0].status)
#print(weekWeather[0].rain)
