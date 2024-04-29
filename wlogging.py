# *************************************************************************************************** 
# ******************************************** WLOGGING *********************************************
# *************************************************************************************************** 

import logging
import pytz
from datetime import datetime
from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

class LogType(Enum):
    INFO = 1
    ERROR = 2

class LogId(Enum):
    INDATA_CHG =  ' INDATA_CHG'
    OUTDATA_CHG = 'OUTDATA_CHG'
    API_CHG =     '    API_CHG'
    API_UPD =     '    API_UPD'
    EXCEPTION =   '  EXCEPTION'

logging.basicConfig(filename='/home/pi/Documents/weather4cast/logs/weather4cast.log', level=logging.INFO)

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 

def log(logType, logId, message):
    madrid_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(madrid_tz)
    log = now.strftime("%H:%M:%S")
    log += ' [' + logId + '] ' + message
    if logType == LogType.INFO.value:
        logging.info(log)
    else:
        logging.error(log)
    print(log)
