# WEATHER4CAST
![image](https://github.com/imanolpadillo/weather4cast/assets/67315499/6c641faf-240b-4e6a-9bad-6b02a9b2b7c2)

## 🗞️ Introduction
This project is focused on developing a weather forecast device based on a Raspberry Pi. More details about HW construction can be found in the following link: TBD.


## 🔌 Weather APIs
Weather4cast works with the following weather APIs:

N. | Name | Name Id | API_KEY? | Refresh | API limit | url 
--- | --- | --- | --- |--- |--- |--- 
1 | foreca | forecapi | yes | 300s (05min) | 1000 calls/day | [https://rapidapi.com/foreca-ltd-foreca-ltd-default/api/foreca-weather](https://rapidapi.com/foreca-ltd-foreca-ltd-default/api/foreca-weather)
2 | meteomatics | metemati | yes | 300s (05min) | 500 calls/day | [https://www.meteomatics.com/en/api/getting-started/](https://www.meteomatics.com/en/api/getting-started/) 
3 | open-meteo | openmete | no | 300s (05min) | none | [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs) 
4 | el-tiempo.net | eltiempo | no | 900s (15min) | none | [https://www.el-tiempo.net/api](https://www.el-tiempo.net/api)
5 | meteoblue | meteblue | yes | 28800s  (8h) | 1250 calls/year| [https://docs.meteoblue.com/en/weather-apis/packages-api/overview](https://docs.meteoblue.com/en/weather-apis/packages-api/overview)
6 | meteostat | metestat | yes | 5400s (1,5h) | 500 calls/month | [https://dev.meteostat.net/api/](https://dev.meteostat.net/api/)
7 | ai weather | aiweathr | yes | 28800s  (8h) | 100 calls/month | [https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/](https://rapidapi.com/MeteosourceWeather/api/ai-weather-by-meteosource/)
8 | visualcrossing | visucros | yes | 300s (05min) | 1000 calls/day | [https://www.visualcrossing.com](https://www.visualcrossing.com)
9 | tomorrow.io | tomorrow | yes | 300s (05min) | 500 calls/day | [https://api.tomorrow.io/](https://api.tomorrow.io/)
10 | openweathermap | openweat | yes | 900s (15min) | 60 calls/min | [https://openweathermap.org/api](https://openweathermap.org/api)
11 | 7timer | 7timer | no | 300s (05min) | none | [https://github.com/Yeqzids/7timer-issues/wiki/Wiki](https://github.com/Yeqzids/7timer-issues/wiki/Wiki)
12 | apimet | apimet | no | 300s (05min) | none | [https://api.met.no/weatherapi/locationforecast/2.0/documentation](https://api.met.no/weatherapi/locationforecast/2.0/documentation)
13 | dummy | dummy | no | 300s (05min) | none | dummy

## 🎮 Action button commands

Buttons:
- Action Button   : A 
- Daily Button    : D
- Hour Button     : H

Legend:
- Single click    : A
- Double click    : AA
- Triple click    : AAA
- x click         : Ax
- Long click      : [A]
- Superlong click : [[A]]

Mode Actions:
- [[A]]           : RST mode
- [A]             : ECO mode
- H[A]            : CLK mode
- HD[A]           : LIFX neutral
- A[A]            : API+
- AA[A]           : API-
- D[A]            : API info
- DDD             : RST day dial
- HHH             : RST hour dial

Weather Actions:
- A               : 0-24h
- AA              : 24-48h
- AAA             : 24-144h
- DAx             : +x days REL
- DDAx            : +x days ABS
- HAx             : +x hours REL
- HHAx            : +x hours ABS
- HDA             : Next rain
- HDDA,DHHA       : 1day rain report
- HDD[A],DHH[A]   : 5day rain report
- HHDDA           : 1day weather report
- HHDD[A]         : 5day weather report

## 🎮 Raspi commands

 0. Get raspi ip
```
ping weather4cast.local
```

 1.  Raspi ssh access
```
ssh pi@192.168.0.10
```

 2. Copy files from PC to Raspi
```
scp /Users/imanolpadillo/Documents/weather4cast/weather4cast/*.* pi@192.168.0.10:/home/pi/Documents/weather4cast
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
0 0 * * 0 > /home/pi/Documents/weather4cast/logs/weather.log
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


## 📶 How to deal WIFI change?
Enter into the following file:
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```
Add at the end of the file the new WIFI network and password
```
network={
    ssid="Network1"
    psk="password1"
}

network={
    ssid="Network2"
    psk="password2"
}
```
