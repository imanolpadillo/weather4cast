# *************************************************************************************************** 
# ********************************************** LIFX ***********************************************
# *************************************************************************************************** 
#Source: https://api.developer.lifx.com/reference/authentication
import requests, os
import configparser

# *************************************************************************************************** 
# CONSTANTS AND GLOBAL VARIABLES
# *************************************************************************************************** 

lifx_scenes = None   # List of saved scenes
script_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file_path = os.path.join(script_dir, 'secrets.ini')
config = configparser.ConfigParser()
config.read(secrets_file_path)

# Your LIFX API token
API_TOKEN = config['secrets']['LIFX_TOKEN']

# The headers including the Authorization token
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
}

def get_lifx_scenes():
    '''
    get all lifx saved scenes
    '''
    global headers
    # Endpoint to list all scenes
    url = "https://api.lifx.com/v1/scenes"
    
    # Make a GET request to fetch scenes
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        scenes = response.json()
        return scenes
    else:
        print(f"Failed to fetch scenes. Status code: {response.status_code}")
        return None

def set_lifx_scene(scene_name):
    '''
    set a lifx saved scene
    input: scene_name (string)
    '''
    global lifx_scenes
    global headers
    scene = next((scene for scene in lifx_scenes if scene['name'] == scene_name), None)
    if scene:
        scene_uuid = scene['uuid']
        url = f"https://api.lifx.com/v1/scenes/scene_id:{scene_uuid}/activate"

        # The payload to set the color to blue
        data = {
            "ignore": ["power"]
        }

        activate_response = requests.put(url, headers=headers, json=data)

        if activate_response.status_code != 207:
            print(f"Failed to activate scene '{scene_name}'. Status code: {activate_response.status_code}")
    else:
        print(f"Scene '{scene_name}' not found.")

def rgb_to_hex(r, g, b):
    '''
    Convert RGB to hexadecimal
    '''
    return f"#{r:02x}{g:02x}{b:02x}"

def set_lifx_color(r, g, b, s):
    '''
    Set LIFX color from RGB input
    '''
    global headers
    # The base URL for the LIFX API
    url = "https://api.lifx.com/v1/lights/all/state"
    # Get hex color
    hex_color = rgb_to_hex(r, g, b)
    # The payload to set the color to blue
    payload = {
        # "power": "on",           # Turn the light on
        "color": hex_color + " saturation:" + str(s),      # Set the color
        "brightness": 0.38,       # Set brightness (0.0 to 1.0)
        "duration": 1.0          # Duration of the transition in seconds
    }

    # Make the request to the LIFX API to change the light color
    response = requests.put(url, headers=headers, json=payload)

    # Check the response
    if response.status_code != 207:  # Multi-Status
        print(f"Failed to set color: {response.status_code} - {response.text}")


lifx_scenes = get_lifx_scenes()
# set_lifx_color(0, 0, 200, 0.8)
set_lifx_scene('stormy')


