# *************************************************************************************************** 
# ******************************************** WLOGGING *********************************************
# *************************************************************************************************** 

import logging, os
import pytz
from datetime import datetime
from enum import Enum

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
    NEXTDAY_RAIN = 'Next day rains warning!'
    API_CHG =      'API_CHG'
    API_UPD =      'API_UPD'
    ERR_API_DATA = 'No API data'
    ERR_API_CONN = 'Unable to connect with API'

# logging.basicConfig(filename='/home/pi/Documents/weather4cast/logs/weather4cast.log', level=logging.INFO)
current_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(filename=current_path+'/logs/weather4cast.log', level=logging.INFO)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def log(logType, logId, message):
    madrid_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(madrid_tz)
    log = now.strftime("%H:%M:%S")
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
