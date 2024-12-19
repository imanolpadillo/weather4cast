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
    RAIN_WARNING_TIME = 2   # limit of hours to check
    RAIN_WARNING_TELEGRAM_ON = True  # If True Telegram notification is send
    MAX_WIND_MS = 12  # max wind speed
    RAIN_STEP = 0.5  # mm that correspond to a row in led matrix
    RAIN_STEP_MODE = WeatherRainStep.AUTO.value  # auto adjust scale of rain
    INTENSITY_7LED = 3  # 7led intensity
    INTENSITY_LED_MATRIX = 10  # led matrix intensity
    ECO_MODE_ON = True  # in 'eco mode' leds are switched off in eco time
    ECO_MODE_INIT_TIME = "22:00"  # 'eco mode' init time
    ECO_MODE_END_TIME = "06:00"  # 'eco mode' end time
    LIFX_ON = True  # If True LIFX color changes with status change

class WeatherStatus(Enum):
    SUNNY = 1
    PARTLY_CLOUDY = 2
    CLOUDY = 3
    RAINY = 4
    STORMY = 5
    WINDY = 6
    FOGGY = 7
    SNOWY = 8

class WeatherLifxColor(Enum):
    SUNNY = (249, 192, 120, 0.5)
    PARTLY_CLOUDY = (249, 192, 120, 0.1)
    CLOUDY = (215, 244, 250, 0.2)
    RAINY = (14, 3, 251, 1.0)
    STORMY = (74, 14, 245, 0.5)
    WINDY = (17, 151, 126, 0.5)
    FOGGY = (1, 23, 33, 0.2)
    SNOWY = (53, 228, 240, 0.9)

class WeatherLifxScenes(Enum):
    SUNNY = 'sunny'
    PARTLY_CLOUDY = 'partly_cloudy'
    CLOUDY = 'cloudy'
    RAINY = 'rainy' 
    STORMY = 'stormy'
    WINDY = 'windy'
    FOGGY = 'foggy'
    SNOWY = 'snowy'

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
    ShortLongClick = 4
    ShortShortLongClick = 5
    LongClick = 6
    SuperLongClick = 7
    CuadrupleClick = 8
    QuintupleClick = 9
    SextupleClick = 10
    SevenfoldClick = 11

class ActionButtonMode(Enum):
    Normal = 0
    WeekDay = 1
    SequentialDay = 2

class DayWeather:
    def __init__(self, status=None, rain=None, temperature=None):
        self.status = status if status is not None else [None]*24
        self.rain = rain if rain is not None else [0.0]*24
        self.temperature = temperature if temperature is not None else [None]*24
