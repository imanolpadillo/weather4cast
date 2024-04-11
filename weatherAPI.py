# *************************************************************************************************** 
# ******************************************* WEATHER API *******************************************
# *************************************************************************************************** 

import requests
from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

NEXT_DAYS = 4

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
                       {'Despejado': WeatherStatus.SUNNY}, \
                       {'Nubes altas': WeatherStatus.PARTLY_CLOUDY}, \
                       {'Intervalos nuboso': WeatherStatus.PARTLY_CLOUDY}, \
                       {'Poco nuboso': WeatherStatus.PARTLY_CLOUDY}, \
                       {'Bruma': WeatherStatus.PARTLY_CLOUDY}, \
                       {'Intervalos nubosos con lluvia escasa': WeatherStatus.PARTLY_CLOUDY}, \
                       {'Muy nuboso': WeatherStatus.CLOUDY}, \
                       {'Cubierto': WeatherStatus.CLOUDY}, \
                       {'Cubierto con lluvia escasa': WeatherStatus.CLOUDY}, \
                       {'Muy nuboso con lluvia escasa': WeatherStatus.CLOUDY}, \
                       {'Nuboso con lluvia': WeatherStatus.RAINY}, \
                       {'Muy nuboso con lluvia': WeatherStatus.RAINY}, \
                       {'nie': WeatherStatus.SNOWY}, \
                       {'tor': WeatherStatus.STORMY}, \
                       {'sol': WeatherStatus.SUNNY}, \
                       {'llu': WeatherStatus.RAINY}, \
                       {'vie': WeatherStatus.FOGGY}, \
                       {'cub': WeatherStatus.CLOUDY}, \
                       {'nub': WeatherStatus.CLOUDY}
                    ]

class DayWeather:
    def __init__(self, status=None, rain=None, temperature=None):
        self.status = status if status is not None else [0]*24
        self.rain = rain if rain is not None else [0]*24
        self.temperature = temperature if temperature is not None else [0]*24

weekWeather = [DayWeather() for _ in range(NEXT_DAYS+2)]  # today + tomorrow + next days

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def call_api():
    """
    calls REST-API from "el-tiempo.net"
    :return: json file
    """ 
    url = 'https://www.el-tiempo.net/api/json/v2/provincias/01/municipios/01059'
    headers = {'cache-control': "no-cache"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def decode_json(data):
    """
    calls REST-API from "el-tiempo.net". Global variable "weekWeather" is updated.
    :param data: json file obtained from "el-tiempo.net" REST-API
    :return: -
    """ 
    # TODAY WEATHER
    # A) Temperature
    weekWeather[0].temperature = data['pronostico']['hoy']['temperatura']
    temperature_len = len(weekWeather[0].temperature)
    # - Fill previous hourly values with actual value
    for x in range(24 - temperature_len):
        weekWeather[0].temperature.insert(0,data['pronostico']['hoy']['temperatura'][0])
    # B) Rain
    weekWeather[0].rain = data['pronostico']['hoy']['precipitacion']
    rain_len = len(weekWeather[0].rain)
    # - Fill previous hourly values with actual value
    for x in range(24 - rain_len):
        weekWeather[0].rain.insert(0,data['pronostico']['hoy']['precipitacion'][0])
    # C) status
    weekWeather[0].status = data['pronostico']['hoy']['estado_cielo_descripcion']
    status_len = len(weekWeather[0].status)
    # - Fill previous hourly values with actual value
    for x in range(24 - status_len):
        weekWeather[0].status.insert(0,data['pronostico']['hoy']['estado_cielo_descripcion'][0])
 
    # TOMORROW WEATHER
    # A) Temperature
    weekWeather[1].temperature = data['pronostico']['manana']['temperatura']
    # B) Rain
    weekWeather[1].rain = data['pronostico']['manana']['precipitacion']
    # C) status
    weekWeather[1].status = data['pronostico']['manana']['estado_cielo_descripcion']
 
    # NEXT 4 DAYS
    for x in range(NEXT_DAYS+1):  #first 'next days' matches with tomorrow and is discarded
        if x==0: continue   
        # A) Temperature
        weekWeather[x+1].temperature = [data['proximos_dias'][x]['temperatura']['minima']]*8 + \
            [data['proximos_dias'][x]['temperatura']['maxima']]*8 + \
            [data['proximos_dias'][x]['temperatura']['minima']]*8
        # B) Rain
        if len(data['proximos_dias'][x]['prob_precipitacion']) == 7:                # [0: 00-24, 1: 00:12, 2: 12-24]
                                                                                    # [3: 00-06, 4: 06:12, 5: 12-18, 6: 18-24]
            weekWeather[x+1].rain = [data['proximos_dias'][x]['prob_precipitacion'][3]]*6 + \
                [data['proximos_dias'][x]['prob_precipitacion'][4]]*6 + \
                [data['proximos_dias'][x]['prob_precipitacion'][5]]*6 + \
                [data['proximos_dias'][x]['prob_precipitacion'][6]]*6
        elif len(data['proximos_dias'][x]['prob_precipitacion']) == 3:              # [0: 00-24, 1: 00:12, 2: 12-24]
            weekWeather[x+1].rain = [data['proximos_dias'][x]['prob_precipitacion'][1]]*12 + \
                [data['proximos_dias'][x]['prob_precipitacion'][2]]*12      
        else:                                                                       # [0: 00-24]
            weekWeather[x+1].rain = [data['proximos_dias'][x]['prob_precipitacion']]*12     
        # C) Status
        if len(data['proximos_dias'][x]['estado_cielo_descripcion']) == 7:          # [0: 00-24, 1: 00:12, 2: 12-24]
                                                                                    # [3: 00-06, 4: 06:12, 5: 12-18, 6: 18-24]
            weekWeather[x+1].status = [data['proximos_dias'][x]['estado_cielo_descripcion'][3]]*6 + \
                [data['proximos_dias'][x]['estado_cielo_descripcion'][4]]*6 + \
                [data['proximos_dias'][x]['estado_cielo_descripcion'][5]]*6 + \
                [data['proximos_dias'][x]['estado_cielo_descripcion'][6]]*6
        elif len(data['proximos_dias'][x]['estado_cielo_descripcion']) == 3:        # [0: 00-24, 1: 00:12, 2: 12-24]
            weekWeather[x+1].status = [data['proximos_dias'][x]['estado_cielo_descripcion'][1]]*12 + \
                [data['proximos_dias'][x]['estado_cielo_descripcion'][2]]*12
        else:                                                                       # [0: 00-24]
            print(data['proximos_dias'][x]['estado_cielo_descripcion'])
            weekWeather[x+1].status = [data['proximos_dias'][x]['estado_cielo_descripcion']]*12
   
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

