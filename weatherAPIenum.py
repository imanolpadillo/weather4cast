from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

DAYS = 6

class WeatherStatus(Enum):
    SUNNY = 1
    PARTLY_CLOUDY = 2
    CLOUDY = 3
    RAINY = 4
    STORMY = 5
    WINDY = 6
    FOGGY = 7
    SNOWY = 8

class DayWeather:
    def __init__(self, status=None, rain=None, temperature=None):
        self.status = status if status is not None else ['-']*24
        self.rain = rain if rain is not None else [0]*24
        self.temperature = temperature if temperature is not None else ['-']*24