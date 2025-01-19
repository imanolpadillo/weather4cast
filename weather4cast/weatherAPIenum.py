from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

class WorkingMode(Enum):
    OFF = '0'
    ON = '1'
    CLOCK = 'C'

class WeatherRainStep(Enum):
    FIXED = 0 # rain step is fixed by RAIN_STEP
    AUTO = 1  # rain step is x2 when rain is > RAIN_STEP*8

class WeatherConfig(Enum):
    GEO_LON = '-2.6724025'  # longitude
    GEO_LAT = '42.8465088'  # latitude
    TIME_ZONE = 'Europe/Madrid'  # time zone
    DAYS = 6   # Number of day to be forecasted
    RAIN_WARNING_REFRESH_TIME = 1   # in seconds
    RAIN_WARNING_MM = 1  # limit of rain mm
    RAIN_WARNING_TIME = 2   # limit of hours to check
    RAIN_WARNING_TELEGRAM_ON = True  # If True Telegram notification is send
    TOMORROW_RAIN_MANUAL_CANCEL = False  # Allow disabling tomorrow manually with x2 click
    MAX_WIND_MS = 14  # max wind speed
    RAIN_STEP = 0.5  # mm that correspond to a row in led matrix
    RAIN_STEP_MODE = WeatherRainStep.AUTO.value  # auto adjust scale of rain
    INTENSITY_7LED_MODE_0N = 1  # 7led intensity in mode on
    INTENSITY_7LED_MODE_CLOCK = 0  # 7led intensity in mode clock
    INTENSITY_LED_MATRIX = 1  # led matrix intensity
    TIMEOUT_24_48_120 = 6   # seconds that 24, 48, 120 display is shown
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
    ECO_MODE_HOLIDAYS_SCHEDULE = "000000011111111111111CCC"
    #                             000000000011111111112222   
    #                             012345678901234567890123  
    ECO_MODE_SCHEDULE = [        "000001100000000111111C00","000001100000000111111C00","000001100000000111111C00",
    # hours                       000000000011111111112222   000000000011111111112222   000000000011111111112222
    #                             012345678901234567890123   012345678901234567890123   012345678901234567890123
                                 "000001100000000111111C00","000001100000000111111CCC","000000011111111111111CCC",
    #                             000000000011111111112222   000000000011111111112222   000000000011111111112222
    #                             012345678901234567890123   012345678901234567890123   012345678901234567890123 
                                 "000000011111111111111C00"]
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
    x01Click = 1
    x02Click = 2
    x03Click = 3
    x04Click = 4
    x05Click = 5
    x06Click = 6
    x07Click = 7
    x08Click = 8
    x09Click = 9
    x10Click = 10
    x11Click = 11
    x12Click = 12
    x13Click = 13
    x14Click = 14
    x15Click = 15
    x16Click = 16
    x17Click = 17
    x18Click = 18
    x19Click = 19
    x20Click = 20
    x21Click = 21
    x22Click = 22
    x23Click = 23
    x24Click = 24
    ShortLongClick = 25
    ShortShortLongClick = 26
    LongClick = 27
    SuperLongClick = 28
	
class ActionButtonMode(Enum):
    Normal = 0
    IncreaseDayAbs = 1
    IncreaseDayRel = 2
    IncreaseHourAbs = 3
    IncreaseHourRel = 4

class DayWeather:
    def __init__(self, status=None, rain=None, temperature=None):
        self.status = status if status is not None else [None]*24
        self.rain = rain if rain is not None else [0.0]*24
        self.temperature = temperature if temperature is not None else [None]*24
