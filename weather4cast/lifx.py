# *************************************************************************************************** 
# ********************************************** LIFX ***********************************************
# *************************************************************************************************** 
#Source: https://api.developer.lifx.com/reference/authentication
import requests, os
import configparser

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

script_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file_path = os.path.join(script_dir, 'secrets.ini')
config = configparser.ConfigParser()
config.read(secrets_file_path)

# Your LIFX API token
API_TOKEN = config['secrets']['LIFX_TOKEN']

# The base URL for the LIFX API
BASE_URL = "https://api.lifx.com/v1/lights/all/state"

# The headers including the Authorization token
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
}

def rgb_to_hex(r, g, b):
    '''
    Function to convert RGB to hexadecimal
    '''
    return f"#{r:02x}{g:02x}{b:02x}"

def set_lifx_color(r, g, b):
    '''
    Function to set LIFX color from RGB input
    '''
    # Get hex color
    hex_color = rgb_to_hex(r, g, b)
    # The payload to set the color to blue
    payload = {
        # "power": "on",           # Turn the light on
        "color": hex_color + " saturation:0.8",      # Set the color
        "brightness": 1.0,       # Set brightness (0.0 to 1.0)
        "duration": 1.0          # Duration of the transition in seconds
    }

    # Make the request to the LIFX API to change the light color
    response = requests.put(BASE_URL, headers=headers, json=payload)

    # Check the response
    if response.status_code == 207:  # Multi-Status
        print("The color has been set.")
    else:
        print(f"Failed to set color: {response.status_code} - {response.text}")

set_lifx_color(20,200,0)