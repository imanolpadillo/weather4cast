# *************************************************************************************************** 
# ************************************* WEATHER API: ELTIEMPO ***************************************
# *************************************************************************************************** 
# Source: https://www.el-tiempo.net/api

import requests, math
from weatherAPIenum import WeatherConfig, WeatherStatus, DayWeather
import wlogging
from wlogging import LogType, LogMessage

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 
 
api_name = 'eltiempo'
api_refresh_s = 300
api_url = 'https://www.el-tiempo.net/api/json/v2/provincias/01/municipios/01059'

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
                       {'Niebla': WeatherStatus.FOGGY}, \
                       {'nie': WeatherStatus.SNOWY}, \
                       {'tor': WeatherStatus.STORMY}, \
                       {'sol': WeatherStatus.SUNNY}, \
                       {'llu': WeatherStatus.RAINY}, \
                       {'vie': WeatherStatus.WINDY}, \
                       {'cub': WeatherStatus.CLOUDY}, \
                       {'nub': WeatherStatus.CLOUDY}
                    ]

weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  # today + tomorrow + next days

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
    
def info_weather_to_rain_mm(day_index):
    """
    Forecast from tomorrow does not include rain_mm. This function translates weather info
    into rain_mm
    """
    for hour in range(24):
        if "lluvia escasa" in weekWeather[day_index].status[hour]:
            weekWeather[day_index].rain[hour] = 0.5
        elif "lluvia" in weekWeather[day_index].status[hour]:
            weekWeather[day_index].rain[hour] = 2
        elif "nieve" in weekWeather[day_index].status[hour]:
            weekWeather[day_index].rain[hour] = 2
        elif "tormenta" in weekWeather[day_index].status[hour]:
            weekWeather[day_index].rain[hour] = 3
        elif int(weekWeather[day_index].rain[hour]) >= 80:
            weekWeather[day_index].rain[hour] = 0.5
        else:
            weekWeather[day_index].rain[hour] = 0

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
    calls REST-API from "el-tiempo.net". Global variable "weekWeather" is updated.
    :param data: json file obtained from "el-tiempo.net" REST-API
    :return: -
    """ 
    global weekWeather
    weekWeather = [DayWeather() for _ in range(WeatherConfig.DAYS.value)]  
    # TODAY WEATHER
    # A) Temperature
    weekWeather[0].temperature = data['pronostico']['hoy']['temperatura']
    temperature_len = len(weekWeather[0].temperature)
    # - Fill previous hourly values with actual value. Except first value (min) and second (max).
    #   This is done for min,max calculation from array.
    for x in range(24 - temperature_len):
        if x==24 - temperature_len -1:
            weekWeather[0].temperature.insert(0,data['temperaturas']['min'])
        elif x==24 - temperature_len -2:
            weekWeather[0].temperature.insert(0,data['temperaturas']['max'])
        else:
            weekWeather[0].temperature.insert(0,data['pronostico']['hoy']['temperatura'][0])
    # B) status
    weekWeather[0].status = data['pronostico']['hoy']['estado_cielo_descripcion']
    status_len = len(weekWeather[0].status)
    # - Fill previous hourly values with actual value
    for x in range(24 - status_len):
        weekWeather[0].status.insert(0,data['pronostico']['hoy']['estado_cielo_descripcion'][0])
    # C) Rain
    today_rain = [float(x) if x.replace('.', '', 1).isdigit() else 0 for x in data['pronostico']['hoy']['precipitacion']]
    weekWeather[0].rain = [round(value,1) for value in today_rain]   
    rain_len = len(weekWeather[0].rain)
    # - Fill previous hourly values with actual value
    for x in range(24 - rain_len):
        weekWeather[0].rain.insert(0,today_rain[0])
 
    # TOMORROW WEATHER
    # A) Temperature
    weekWeather[1].temperature = data['pronostico']['manana']['temperatura']
    # B) status
    weekWeather[1].status = data['pronostico']['manana']['estado_cielo_descripcion']
    # C) Rain
    tomorrow_rain = [float(x) if x.replace('.', '', 1).isdigit() else 0 for x in data['pronostico']['manana']['precipitacion']]
    weekWeather[1].rain = [round(value,1) for value in tomorrow_rain]   
 
    # NEXT 4 DAYS
    for x in range(WeatherConfig.DAYS.value-1):  #first 'next days' matches with tomorrow and is discarded
        if x==0: continue 
        # A) Temperature
        weekWeather[x+1].temperature = [data['proximos_dias'][x-1]['temperatura']['minima']]*8 + \
            [data['proximos_dias'][x-1]['temperatura']['maxima']]*8 + \
            [data['proximos_dias'][x-1]['temperatura']['minima']]*8
        # B) Status
        if len(data['proximos_dias'][x-1]['estado_cielo_descripcion']) == 7:          # [0: 00-24, 1: 00:12, 2: 12-24]
                                                                                    # [3: 00-06, 4: 06:12, 5: 12-18, 6: 18-24]
            weekWeather[x+1].status = [data['proximos_dias'][x-1]['estado_cielo_descripcion'][3]]*6 + \
                [data['proximos_dias'][x-1]['estado_cielo_descripcion'][4]]*6 + \
                [data['proximos_dias'][x-1]['estado_cielo_descripcion'][5]]*6 + \
                [data['proximos_dias'][x-1]['estado_cielo_descripcion'][6]]*6
        elif len(data['proximos_dias'][x-1]['estado_cielo_descripcion']) == 3:        # [0: 00-24, 1: 00:12, 2: 12-24]
            weekWeather[x+1].status = [data['proximos_dias'][x-1]['estado_cielo_descripcion'][1]]*12 + \
                [data['proximos_dias'][x-1]['estado_cielo_descripcion'][2]]*12
        else:                                                                       # [0: 00-24]
            weekWeather[x+1].status = [data['proximos_dias'][x-1]['estado_cielo_descripcion']]*24
        # C) Rain
        if len(data['proximos_dias'][x-1]['prob_precipitacion']) == 7:                # [0: 00-24, 1: 00:12, 2: 12-24]
                                                                                    # [3: 00-06, 4: 06:12, 5: 12-18, 6: 18-24]
            weekWeather[x+1].rain = [data['proximos_dias'][x-1]['prob_precipitacion'][3]]*6 + \
                [data['proximos_dias'][x-1]['prob_precipitacion'][4]]*6 + \
                [data['proximos_dias'][x-1]['prob_precipitacion'][5]]*6 + \
                [data['proximos_dias'][x-1]['prob_precipitacion'][6]]*6
        elif len(data['proximos_dias'][x-1]['prob_precipitacion']) == 3:              # [0: 00-24, 1: 00:12, 2: 12-24]
            weekWeather[x+1].rain = [data['proximos_dias'][x-1]['prob_precipitacion'][1]]*12 + \
                [data['proximos_dias'][x-1]['prob_precipitacion'][2]]*12      
        else:                                                                       # [0: 00-24]
            weekWeather[x+1].rain = [data['proximos_dias'][x-1]['prob_precipitacion']]*24
        info_weather_to_rain_mm(x+1)    

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
# print("ELTIEMPO")
# print(weekWeather[0].temperature)
# print(weekWeather[0].status)
# print(weekWeather[0].rain)
