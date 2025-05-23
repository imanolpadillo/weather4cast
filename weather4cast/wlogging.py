# *************************************************************************************************** 
# ******************************************** WLOGGING *********************************************
# *************************************************************************************************** 

import logging, os
import pytz
from datetime import datetime
from enum import Enum
from weatherAPIenum import WeatherConfig

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

LOGID_MAX_LEN = 13

class LogType(Enum):
    INFO = 1
    ERROR = 2

class LogMessage(Enum):
    SWITCH_ON =    'Starting weather4cast!'
    INDATA_CHG =   'INDATA_CHG'
    OUTDATA_CHG =  'OUTDATA_CHG'
    API_CHG =      'API_CHG'
    API_UPD =      'API_UPD'
    ERR_API_DATA = 'No API data'
    ERR_API_CONN = 'Unable to connect with API'
    ERR_LIFX =     'Unable to connect with LIFX'
    ECO_MODE_ON =  'ECO MODE: ON activated'
    ECO_MODE_OFF = 'ECO MODE: OFF activated'
    ECO_MODE_CLK = 'ECO MODE: CLOCK activated'
    MAN_MODE_OFF1 = 'MANUAL MODE OFF: activated'
    MAN_MODE_OFF0 = 'MANUAL MODE OFF: deactivated'
    MAN_MODE_CLK1 = 'MANUAL MODE CLOCK: activated'
    MAN_MODE_CLK0 = 'MANUAL MODE CLOCK: deactivated'
    LIFX_CHG =     'LIFX_CHG'
    TELEGRAM_SND = 'TELEGRAM sent'

# logging.basicConfig(filename='/home/pi/Documents/weather4cast/logs/weather4cast.log', level=logging.INFO)
current_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=current_path+'/logs/weather4cast.log', level=logging.INFO)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def log(logType, logId, message):
    now = datetime.now(pytz.timezone(WeatherConfig.TIME_ZONE.value))
    log = now.strftime("%Y-%m-%d %H:%M:%S")
    if logType == LogType.ERROR.value: 
        logidlength = LOGID_MAX_LEN - 1
    else:
        logidlength = LOGID_MAX_LEN
    while len(logId) < logidlength:
        logId = ' ' + logId
    log += ' [' + logId + '] ' + message
    if logType == LogType.INFO.value:
        logging.info(log)
    else:
        logging.error(log)
    print(log)
