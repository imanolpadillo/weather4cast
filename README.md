# WEATHER4CAST
![image](https://github.com/imanolpadillo/weather4cast/assets/67315499/6c641faf-240b-4e6a-9bad-6b02a9b2b7c2)

## 🗞️ Introduction
This project is focused on developing a weather forecast device based on a Raspberry Pi. More details about HW construction can be found in the following link: TBD.

## 🔌 Weather APIs
Weather4cast works with the following weather APIs:

1. API1: open-meteo
  - url: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)
2. API2: el-tiempo.net
  - url: [https://www.el-tiempo.net/api](https://www.el-tiempo.net/api)
3. API3: visualcrossing -> requires API_KEY
  - url: [https://www.visualcrossing.com](https://www.visualcrossing.com)
4. API4: api.tomorrow.io -> requires API_KEY
  - url: [https://api.tomorrow.io/](https://api.tomorrow.io/)
5. API5: openweathermap -> requires API_KEY
  - url: [https://openweathermap.org/api](https://openweathermap.org/api)
6. API6: meteoblue -> requires API_KEY
  - url: [https://docs.meteoblue.com/en/weather-apis/packages-api/overview](https://docs.meteoblue.com/en/weather-apis/packages-api/overview)
7. API7: meteomatics -> requires API_KEY
  - url: [https://www.meteomatics.com/en/api/getting-started/](https://www.meteomatics.com/en/api/getting-started/)

## 🎮 Raspi commands

 1.  Raspi ssh access
```
ssh pi@192.168.0.41
```

 2. Copy files from PC to Raspi
```
scp /Users/imanolpadillo/Documents/weather4cast/*.* pi@192.168.0.41:/home/pi/Documents/weather4cast
````

 3. Execute weather4cast manually from Raspi
```
cd /home/pi/Documents/weather4cast
python3 main.py
```

 4. Kill weather4cast program
```
ps aux | grep main.py
kill -7 process_id
```

 5. Program a cron for executing weather4cast on restart and delete logs every week
```
sudo crontab -e -u pi
@reboot sh /home/pi/Documents/weather4cast/launcher.sh >/home/pi/Documents/weather4cast/logs/cron.log 2>&1
0 0 * * 0 /bin/rm -f /home/pi/Documents/weather4cast/logs/*
```

 6. Read Raspi logs
```
cd /home/pi/Documents/weather4cast/logs
cat weather4cast.log
```

## 🔏 SECRETS
For those APIs that requires an api-key it is necessary to include in parent path a 'secrets.ini' including the following info:
```
[secrets]
api3_key = XXXXXX
api4_key = XXXXXX
```

## 🆕 Add new API
 - Create 'weatherAPIX.py'
 - In 'weather.py': a) import weatherAPIX b) modify api_weather_names and c) add new api output in functions 'get_current_weather_api()' and 'change_weather_api()' 

