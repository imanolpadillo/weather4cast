# WEATHER4CAST
![image](https://github.com/imanolpadillo/weather4cast/assets/67315499/6c641faf-240b-4e6a-9bad-6b02a9b2b7c2)

## 🗞️ Introduction
This project is focused on developing a weather forecast device based on a Raspberry Pi. More details about HW construction can be found in the following link: TBD.

## 🔌 Weather APIs
Weather4cast works with the following weather APIs:

1. **meteomatics** -> requires API_KEY
  - url: [https://www.meteomatics.com/en/api/getting-started/](https://www.meteomatics.com/en/api/getting-started/)
  - refresh_time: 900s (15min), api_calls_limit: 500 calls/day
2. **foreca** -> requires API_KEY
  - url: [https://rapidapi.com/foreca-ltd-foreca-ltd-default/api/foreca-weather](https://rapidapi.com/foreca-ltd-foreca-ltd-default/api/foreca-weather)
  - refresh_time: 900s (15min), api_calls_limit: 1000 calls/day
3. **open-meteo**
  - url: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)
  - refresh_time: 900s (15min), api_calls_limit: none
4. **el-tiempo.net**
  - url: [https://www.el-tiempo.net/api](https://www.el-tiempo.net/api)
  - refresh_time: 900s (15min), api_calls_limit: none
5. **meteoblue** -> requires API_KEY
  - url: [https://docs.meteoblue.com/en/weather-apis/packages-api/overview](https://docs.meteoblue.com/en/weather-apis/packages-api/overview)
  - refresh_time: 28800s  (8h), api_calls_limit: 1250 calls/year
6. **meteostat** -> requires API_KEY
  - url: [https://dev.meteostat.net/api/](https://dev.meteostat.net/api/)
  - refresh_time: 5400s (1,5h), api_calls_limit: 500 calls/month
7. **aiweathr** -> requires API_KEY
  - url: [https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/](https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/)
  - refresh_time: 28800s  (8h), api_calls_limit: 100 calls/month
8. **visualcrossing** -> requires API_KEY
  - url: [https://www.visualcrossing.com](https://www.visualcrossing.com)
  - refresh_time: 900s (15min), api_calls_limit: 1000 calls/day
9. **tomorrow.io** -> requires API_KEY
  - url: [https://api.tomorrow.io/](https://api.tomorrow.io/)
  - refresh_time: 900s (15min), api_calls_limit: 500 calls/day
10. **openweathermap** -> requires API_KEY
  - url: [https://openweathermap.org/api](https://openweathermap.org/api)
  - refresh_time: 900s (15min), api_calls_limit: 60 calls/min


## 🎮 Raspi commands

 1.  Raspi ssh access
```
ssh pi@192.168.0.41
```

 2. Copy files from PC to Raspi
```
scp /Users/imanolpadillo/Documents/weather4cast/weather4cast/*.* pi@192.168.0.25:/home/pi/Documents/weather4cast
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
visucros = XXXXXX
tomorrow = XXXXXX
```

## 🆕 Add new API
Create 'weatherAPIX.py'. Every weatherAPIX file will be added alphabetically as a new weather API.

