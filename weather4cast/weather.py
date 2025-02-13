# *************************************************************************************************** 
# ********************************************* WEATHER  ********************************************
# *************************************************************************************************** 
import importlib, os, math
from weatherAPIenum import WeatherConfig, WeatherTimeLine
from collections import Counter

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# ***************************************************************************************************
weatherAPI = None
api_weather_id = 1
weatherAPInames = []  # weatherAPI files are ordered alphabetically. Names are saved in this array.
weather_timeline = WeatherTimeLine.T16

def count_weather_apis():
    """
    counts the amount of weatherAPI files (files in current path starting with 'weatherAPI').
    :return: number of weatherAPIs
    """
    global weatherAPInames
    directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of main.py
    count = 0
    for filename in sorted(os.listdir(directory)):
        if (filename.startswith('weatherAPI') and 
            not filename.startswith('weatherAPIenum') and 
            not filename.startswith('weatherAPIchange') and 
            os.path.isfile(os.path.join(directory, filename))):
            weatherAPInames.append(filename.split('.')[0]) # remove suffiy
            count += 1
    return count

MAX_APIS = count_weather_apis()

# *************************************************************************************************** 
# FUNCTIONS
# *************************************************************************************************** 
def get_weather_api_module(weather_api_index):
    """
    imports a weatherAPI file depending on input index.
    :param weather_api_index: integer indicating weatherAPI index
    :return: weatherAPI module
    """
    global weatherAPInames
    module_name = weatherAPInames[weather_api_index-1]
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        print(f"Module {module_name} not found.")
        return None

def get_current_weather_api():
    """
    returns current weather api based on actived api_weather_id
    """
    global api_weather_id
    return get_weather_api_module(api_weather_id)

def get_current_weather_api_name():
    """
    returns current weather api name based on actived api_weather_id
    """
    weatherAPI = get_current_weather_api()
    return weatherAPI.api_name

def get_current_weather_api_refresh_s():
    """
    returns current weather api refresh time based on actived api_weather_id
    """
    weatherAPI = get_current_weather_api()
    return weatherAPI.api_refresh_s

# Change weather api
def change_weather_api(increase = True):
    """
    increases weather_api_id
    """
    global api_weather_id
    if increase == True:
        if api_weather_id < MAX_APIS:
            api_weather_id += 1
        else:
            api_weather_id = 1
    else:
        if api_weather_id <= 1:
            api_weather_id = MAX_APIS
        else:
            api_weather_id -= 1

def refresh():
    """
    calls REST-API and converts json into appropiate information for global variable
    'weekStatus'
    """
    try:
        global weatherAPI
        weatherAPI = get_current_weather_api()
        data = weatherAPI.call_api()
        weatherAPI.decode_json(data)    
    except Exception as e:
        return
    
def get_status (forecast_day, forecast_hour, weather_timeline = WeatherTimeLine.T16):
    """
    gets status of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :param mode: if True returns the mode value of the day
    :return: status
    """
    global weatherAPI
    status_arr = []
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    if weather_timeline == WeatherTimeLine.T16:
        return weatherAPI.weekWeather[forecast_day].status[forecast_hour]
    else:
        if weather_timeline == WeatherTimeLine.T48:
            if forecast_day<WeatherConfig.DAYS.value-1: forecast_day += 1

        if weather_timeline != WeatherTimeLine.T120:
            status_arr = weatherAPI.weekWeather[forecast_day].status
        else:
            for day in range(1,WeatherConfig.DAYS.value):
                status_arr+=weatherAPI.weekWeather[day].status 

        status_counts = Counter(status_arr)
        most_common_element, most_common_count = status_counts.most_common(1)[0]
        return most_common_element

def get_min_max_temperature (forecast_day, weather_timeline = WeatherTimeLine.T16):
    """
    gets min and max temperature of input forecast day
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :return: [tmin,tmax]
    """
    global weatherAPI
    temperature_arr = []
    if weather_timeline == WeatherTimeLine.T48:
        if forecast_day<WeatherConfig.DAYS.value-1: forecast_day += 1

    if weather_timeline != WeatherTimeLine.T120:
        temperature_arr = weatherAPI.weekWeather[forecast_day].temperature
    else:
        for day in range(1,WeatherConfig.DAYS.value):
            temperature_arr+=weatherAPI.weekWeather[day].temperature 
    
    tmin = min(list(map(int, temperature_arr)))
    tmax = max(list(map(int, temperature_arr)))    
    return [tmin, tmax]

def get_temperature (forecast_day, forecast_hour, weather_timeline = WeatherTimeLine.T16):
    """
    gets temperature of input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :param average: if True returns the average value of the day
    :return: temperature
    """
    global weatherAPI
    temperature_arr = []
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    if weather_timeline == WeatherTimeLine.T16:
        return weatherAPI.weekWeather[forecast_day].temperature[forecast_hour]
    else:
        if weather_timeline == WeatherTimeLine.T48:
            if forecast_day<WeatherConfig.DAYS.value-1: forecast_day += 1

        if weather_timeline != WeatherTimeLine.T120:
            temperature_arr = weatherAPI.weekWeather[forecast_day].temperature
        else:
            for day in range(1,WeatherConfig.DAYS.value):
                temperature_arr+=weatherAPI.weekWeather[day].temperature 

        temperature_arr_int = [int(element) for element in temperature_arr]
        temperature_sum = sum(temperature_arr_int)
        return int(temperature_sum/len(temperature_arr_int))


def get_rain (forecast_day, forecast_hour, weather_timeline = WeatherTimeLine.T16):
    """
    gets rain from input forecast day/hour
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: rain array
    """
    global weatherAPI
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    hour_counter=0
    rain_data = []
    for day in range(WeatherConfig.DAYS.value):
        # for hour in range(24):
        for hour in range(len(weatherAPI.weekWeather[day].rain)):
            rain_data.append(weatherAPI.weekWeather[day].rain[hour])
            hour_counter+=1
    # get current index
    index=0
    hour_limit=0
    if weather_timeline==WeatherTimeLine.T16:
        hour_limit=16
        index = forecast_day * 24 + forecast_hour
    elif weather_timeline==WeatherTimeLine.T120:
        hour_limit=120
        index = 24
    else: #T24 + T48
        hour_limit=24
        if weather_timeline==WeatherTimeLine.T48:
            if forecast_day<WeatherConfig.DAYS.value-1: forecast_day += 1
        index = forecast_day * 24
    
    # from index count 16, 24 or 120 rain values
    rain_output = []
    for hour in range(index, len(rain_data)):
        if hour>=hour_limit+index:
            break
        rain_output.append(rain_data[hour])

    # fill with '0.0' if array´s size is lower than hour limit
    while(len(rain_output)<hour_limit):
        rain_output.append(0.0)

    # adjust rain array to size 16
    if len(rain_output)==24:
        rain_output = rain_24_to_16_hours(rain_output)
    elif len(rain_output)==120:
        rain_output = rain_120_to_16_hours(rain_output)

    return rain_output

def rain_24_to_16_hours(input_array, worst_case = True):
    """
    converts 24 array into 16 array
    :param input_array: size 24
    :return: array size 16
    """
    if len(input_array) != 24:
        raise ValueError("Input array must have 24 elements.")
    output_array = []
    if worst_case == True:
        # Worst case
        # Process chunks of 3 elements
        for i in range(0, len(input_array), 3):  # Step through the input array in chunks of 3
            chunk = input_array[i:i + 3]  # Extract the current chunk of 3 elements
            # Sort in descending order, but keep the order as it appears in the input
            largest_two = sorted(chunk, reverse=True)[:2]  # Get the two largest values
            # Now, to maintain order, add the two largest elements in the order they appear in the chunk
            for val in chunk:
                if val in largest_two:
                    output_array.append(val)
                    largest_two.remove(val)
    else:
        # Average
        for i in range(0, len(input_array), 3):
            # Calculate the average of each pair of 1.5 groups
            avg1 = round((input_array[i] + input_array[i+1]) / 2,1)
            avg2 = round((input_array[i+1] + input_array[i+2]) / 2,1)
            output_array.extend([avg1, avg2])
    return output_array

def rain_120_to_16_hours(input_array, worst_case = True):
    """
    converts 120 array into 16 array
    :param input_array: size 120
    :return: array size 16
    """
    if len(input_array) != 120:
        raise ValueError("Input array must have exactly 120 fields.")
    output_array = []
    if worst_case == True:
        # Worst case
        for i in range(0, len(input_array), 8):  # Step through the array in steps of 8
            chunk = input_array[i:i + 8]  # Get the current chunk of 8 elements
            max_value = max(chunk)       # Find the maximum value in the chunk
            output_array.append(max_value)  # Append the max value to the output array
    else:
        # Average
        for i in range(0, len(input_array), 8):
            chunk = input_array[i:i+8]
            chunk_average = sum(chunk) / len(chunk)
            output_array.append(round(chunk_average,1))
    # Append 0 at the end of the output array
    output_array.append(0)
    print(output_array)
    return output_array

def get_next_start_stop_rain_hour (forecast_day, forecast_hour, rain_index, rain_start):
    """
    gets hour for next start/stop rain from input forecast day/hour.
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :return: next_rain_day, next_rain_hour
    """
    global weatherAPI
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)

    hour_counter=0
    rain_data = []
    for day in range(WeatherConfig.DAYS.value):
        # for hour in range(24):
        for hour in range(len(weatherAPI.weekWeather[day].rain)):
            rain_data.append(weatherAPI.weekWeather[day].rain[hour])
            hour_counter+=1

    # get current index
    index = forecast_day * 24 + forecast_hour

    if rain_start == True:
        # if currently raining increase rain_index, for searching first time for next (no current) rain
        if round_to_step(weatherAPI.weekWeather[forecast_day].rain[forecast_hour]) >= WeatherConfig.RAIN_STEP.value:
            rain_index+=1
        # get next_rain_start_index
        next_rain_index = -1
        rain_loop = rain_index
        while (rain_loop > 0):
            next_rain_index=-1
            # search when it starts raining
            for hour in range(index, len(rain_data)):
                if round_to_step(rain_data[hour]) >= WeatherConfig.RAIN_STEP.value:
                    next_rain_index = hour
                    break
            # search when it stops raining
            index = -1
            for hour in range(next_rain_index, len(rain_data)):
                if round_to_step(rain_data[hour]) < WeatherConfig.RAIN_STEP.value:
                    index = hour
                    break
            rain_loop -= 1
    else:
        # if currently not raining increase rain_index, for searching first time for next (no current) end of rain
        if round_to_step(weatherAPI.weekWeather[forecast_day].rain[forecast_hour]) < WeatherConfig.RAIN_STEP.value:
            rain_index+=1
        # get next_rain_stop_index
        next_rain_index = -1
        rain_loop = rain_index
        while (rain_loop > 0):
            next_rain_index=-1
            # search when it stops raining
            for hour in range(index, len(rain_data)):
                if round_to_step(rain_data[hour]) < WeatherConfig.RAIN_STEP.value:
                    next_rain_index = hour
                    break
            # search when it starts raining
            index = -1
            for hour in range(next_rain_index, len(rain_data)):
                if round_to_step(rain_data[hour]) >= WeatherConfig.RAIN_STEP.value:
                    index = hour
                    break
            rain_loop -= 1     
        

    # exit with -1 if no next rain    
    if next_rain_index == -1:
        return -1,-1

    # get next_rain_hour and next_rain_day
    next_rain_day = next_rain_index // 24
    next_rain_hour = next_rain_index % 24

    return next_rain_day, next_rain_hour


def get_rain_report (forecast_day):
    """
    gets hours with rain
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :return: string indicating hour + rain
    """
    global weatherAPI
    report = ''
    for hour in range(24):
        if weatherAPI.weekWeather[int(forecast_day)].rain[hour] > 0:
            # hour always with 2 digits
            hour_str = str(hour).zfill(2)
            report += '\n' + hour_str + 'h: ' + str(weatherAPI.weekWeather[int(forecast_day)].rain[hour]) + 'mm/h'
    return report

def get_weather_report (forecast_day):
    """
    gets rain + temperature + status for input day
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :return: string indicating hour + rain + temperature + status
    """
    global weatherAPI
    report = ''
    for hour in range(24):
        # hour always with 2 digits
        hour_str = str(hour).zfill(2)
        # get hour data
        rain = weatherAPI.weekWeather[int(forecast_day)].rain[hour]
        temperature = weatherAPI.weekWeather[int(forecast_day)].temperature[hour]
        status = weatherAPI.weekWeather[int(forecast_day)].status[hour].name
        report += '\n' + hour_str + 'h: ' + str(rain) + 'mm/h, ' + \
            str(temperature).rjust(2, ' ')+ '°C, ' + str(status)
    return report

def round_to_step(input_value, step = WeatherConfig.RAIN_STEP.value):
    """
    Rounds each input_value to the nearest multiple of the step.
   
    Args:
    - step (float): The step size to round to.
    - input_value: Input values to round.
   
    Returns:
    - list of floats: The rounded values.
    """
    rounded_value = round(input_value / step) * step 
    return rounded_value
  
def get_rain_warning(forecast_day, forecast_hour, rain_limit, hour_limit, weather_timeline = WeatherTimeLine.T16):
    """
    returns true, if rain value is higher than rain_limit from next hour
    to the next amount of hours defined by hour_limit
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :param forecast_hour: integer indicating forecast hour (0= 00:00, 1=01:00...)
    :rain_limit: mm that are considered as rain warning
    :hour_limit: hours to be monitored from forecast_day+forecast_hour
    :return: True if it rains the following hours
    """
    global weatherAPI
    raining_flag=False
    raining_quantity=""
    forecast_day = int(forecast_day)
    forecast_hour = int(forecast_hour)
    hour_counter=0
    if weather_timeline!=WeatherTimeLine.T16:
        return raining_flag, raining_quantity, hour_counter
    # join all temperature values
    rain_data = []
    for day in range(WeatherConfig.DAYS.value):
        # for hour in range(24):
        for hour in range(len(weatherAPI.weekWeather[day].rain)):
            rain_data.append(weatherAPI.weekWeather[day].rain[hour])
            hour_counter+=1
    # get current index
    index = forecast_day * 24 + forecast_hour

    # from index, check if it rains the following 'hour_limit' hours.
    raining_quantity = []
    hour_counter=0
    for hour in range(index, len(rain_data)):
        if (hour_counter>hour_limit) and raining_flag == False:
            break
        if round_to_step(rain_data[hour]) >= rain_limit or (raining_flag == True and round_to_step(rain_data[hour]) > 0):
            # continue for until rain != 0
            raining_flag = True
        elif hour_counter>hour_limit:
            break
        raining_quantity.append(rain_data[hour])
        hour_counter+=1
    return raining_flag, raining_quantity, hour_counter

def get_tomorrow_rain(forecast_day, rain_limit):
    """
    returns true, if max rain value for day after forecast_day is higher than rain_limit
    :param forecast_day: integer indicating forecast day (0= today, 1=tomorrow...)
    :rain_limit: mm that are considered as rain warning
    :return: True if it rains next day
    """
    global weatherAPI
    forecast_day = int(forecast_day)

    if forecast_day >= WeatherConfig.DAYS.value -1:
        return False
    else:
        tomorrow_rain = weatherAPI.weekWeather[forecast_day + 1].rain  
        tomorrow_rain_rnd  = [round_to_step(x) for x in tomorrow_rain] 
    rain_max = max(list(map(float, tomorrow_rain_rnd)))
    if rain_max >= rain_limit:
        return True
    else:
        return False
