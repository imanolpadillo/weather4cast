from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

class WeatherRainStep(Enum):
    FIXED = 0 # rain step is fixed by RAIN_STEP
    AUTO = 1  # rain step is x2 when rain is > RAIN_STEP*8

class WeatherConfig(Enum):
    DAYS = 6        # Number of day to be forecasted
    WEATHER_API_REFRESH_TIME = 1800 # in seconds
    RAIN_WARNING_REFRESH_TIME = 1   # in seconds
    RAIN_WARNING_MM = 1  # limit of rain mm
    RAIN_WARNING_TIME = 3   # limit of hours to check
    MAX_WIND_MS = 12  # max wind speed
    RAIN_STEP = 0.5  # mm that correspond to a row in led matrix
    RAIN_STEP_MODE = WeatherRainStep.AUTO.value  # auto adjust scale of rain
    INTENSITY_7LED = 3  # 7led intensity
    INTENSITY_LED_MATRIX = 10  # led matrix intensity
    ECO_MODE_ON = True  # in 'eco mode' keds are switched off in eco time
    ECO_MODE_INIT_HOUR = 22  # 'eco mode' init hour
    ECO_MODE_END_HOUR = 7  # 'eco mode' end hour 

class WeatherStatus(Enum):
    SUNNY = 1
    PARTLY_CLOUDY = 2
    CLOUDY = 3
    RAINY = 4
    STORMY = 5
    WINDY = 6
    FOGGY = 7
    SNOWY = 8

class WeatherTimeLine(Enum):
    T16 = 16    # default
    T24 = 24    # short click: daily 24h
    T48 = 48    # double click: daily 24h of day+1
    T120 = 120  # tripple click: next 5 days

class WeatherButton(Enum):
    NoClick = 0
    ShortClick = 1
    DoubleClick = 2
    TrippleClick = 3
    LongClick = 4
    ShortLongClick = 5
    SuperLongClick = 6
    UltraLongClick = 7

class DayWeather:
    def __init__(self, status=None, rain=None, temperature=None):
        self.status = status if status is not None else [None]*24
        self.rain = rain if rain is not None else [0.0]*24
        self.temperature = temperature if temperature is not None else [None]*24
