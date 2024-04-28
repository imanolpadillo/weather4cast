from enum import Enum

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

# class gpio(Enum):
#     KY040_HOUR_CLK = 24
#     KY040_HOUR_DT = 17
#     KY040_HOUR_SW = 27
#     KY040_DAY_CLK = 6
#     KY040_DAY_DT = 19
#     KY040_DAY_SW = 26
#     MAX7219_DIN = 10
#     MAX7219_CS = 8
#     MAX7219_CLK = 11
#     PCF8574_SDA = 2
#     PCF8574_SCL = 3
#     SWITCH_DAY = 25
#     SWITCH_HOUR = 16
#     TM1637_TMIN_CLK = 5
#     TM1637_TMIN_DIO = 4
#     TM1637_TMAX_CLK = 21
#     TM1637_TMAX_DIO = 20

class gpio(Enum):
    PCF8574_SDA = 2
    PCF8574_SCL = 3
    TM1637_TMIN_DIO = 4
    TM1637_TMIN_CLK = 5
    KY040_DAY_CLK = 6
    MAX7219_CS = 8
    MAX7219_DIN = 10
    MAX7219_CLK = 11
    SWITCH_HOUR = 16
    KY040_HOUR_DT = 17
    KY040_DAY_DT = 19
    TM1637_TMAX_DIO = 20
    TM1637_TMAX_CLK = 21
    KY040_HOUR_CLK = 24
    SWITCH_DAY = 25
    KY040_DAY_SW = 26
    KY040_HOUR_SW = 27
    
