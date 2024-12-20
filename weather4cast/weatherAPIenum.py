from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

class WeatherRainStep(Enum):
    FIXED = 0 # rain step is fixed by RAIN_STEP
    AUTO = 1  # rain step is x2 when rain is > RAIN_STEP*8

class WeatherConfig(Enum):
    GEO_LON = '-2.6724025'  # longitude
    GEO_LAT = '42.8465088'  # latitude
    DAYS = 6   # Number of day to be forecasted
    WEATHER_API_REFRESH_TIME = 1800 # in seconds
    RAIN_WARNING_REFRESH_TIME = 1   # in seconds
    RAIN_WARNING_MM = 1  # limit of rain mm
    RAIN_WARNING_TIME = 2   # limit of hours to check
    RAIN_WARNING_TELEGRAM_ON = True  # If True Telegram notification is send
    MAX_WIND_MS = 12  # max wind speed
    RAIN_STEP = 0.5  # mm that correspond to a row in led matrix
    RAIN_STEP_MODE = WeatherRainStep.AUTO.value  # auto adjust scale of rain
    INTENSITY_7LED = 1  # 7led intensity
    INTENSITY_LED_MATRIX = 2  # led matrix intensity
    LIFX_ON = True  # If True LIFX color changes with status change
    ECO_MODE_ON = True  # in 'eco mode' leds are switched off in eco time
    ECO_MODE_HOLIDAYS = [
        # (month, day)
        # Xmas
        (12, 24), 
        (12, 25), 
        (12, 26), 
        (12, 27),
        (12, 28),
        (12, 29),
        (12, 30),
        (12, 31),
        (1, 1), 
        (1, 2), 
        (1, 3), 
        (1, 4), 
        (1, 5),
        (1, 6), 
        # Summer
        (8, 4), 
        (8, 5), 
        (8, 6), 
        (8, 7), 
        (8, 8), 
        (8, 9), 
        # Spanish National Holidays
        (5, 1), 
        (8, 15), 
        (10, 12),
        (11, 1),
        (12, 6), 
    ]
    ECO_MODE_HOLIDAYS_SCHEDULE = "000000011111111111111000"
    #                             000000000011111111112222   
    #                             012345678901234567890123  
    ECO_MODE_SCHEDULE = [        "000000000000000111111000","000000000000000111111000","000000000000000111111000",
    # hours                       000000000011111111112222   000000000011111111112222   000000000011111111112222
    #                             012345678901234567890123   012345678901234567890123   012345678901234567890123
                                 "000000000000000111111000","000000000000000111111000","000000011111111111111000",
    #                             000000000011111111112222   000000000011111111112222   000000000011111111112222
    #                             012345678901234567890123   012345678901234567890123   012345678901234567890123 
                                 "000000011111111111111000"]
    #                             000000000011111111112222   
    #                             012345678901234567890123 

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
