from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

class WeatherConfig(Enum):
    DAYS = 6        # Number of day to be forecasted
    WEATHER_API_REFRESH_TIME = 1800 # in seconds
    RAIN_WARNING_REFRESH_TIME = 1   # in seconds
    RAIN_WARNING_MM = 1  # limit of rain mm
    RAIN_WARNING_TIME = 3   # limit of hours to check

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
        self.status = status if status is not None else [None]*24
        self.rain = rain if rain is not None else [0.0]*24
        self.temperature = temperature if temperature is not None else [None]*24