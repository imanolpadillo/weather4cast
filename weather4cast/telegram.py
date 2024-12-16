# ***************************************************************************************************
# ******************************************** TELEGRAM *********************************************
# ***************************************************************************************************
 
# STEP1: Create bot
# In Telegram chat '/newbot' to @BotFather in order to create a new bot
 
# STEP2: Add created bot to the chat where messages will be received
 
# STEP3: Get 'chat id' using the following code:
# import requests
# TOKEN = "here paste the bot token provided by @BotFather"
# url = fhttps://api.telegram.org/bot{TOKEN}/getUpdates
# print(requests.get(url).json())
 
import requests, os
import configparser
 
script_dir = os.path.dirname(os.path.abspath(__file__))
secrets_file_path = os.path.join(script_dir, 'secrets.ini')
config = configparser.ConfigParser()
config.read(secrets_file_path)
 
# Your Telegram token
TELEGRAM_TOKEN = config['secrets']['TELEGRAM_TOKEN']
TELEGRAM_CHAT_ID = config['secrets']['TELEGRAM_CHAT_ID']
 
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    print(requests.get(url).json()) # this sends the message
 