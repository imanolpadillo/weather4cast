# WEATHER4CAST
![image](https://github.com/imanolpadillo/weather4cast/assets/67315499/6c641faf-240b-4e6a-9bad-6b02a9b2b7c2)

## 🗞️ Introduction
This project is focused on developing a weather forecast device based on a Raspberry Pi. More details about HW construction can be found in the following link: TBD.

## 🔌 Weather APIs
Weather4cast works with the following weather APIs:

1. API1: el-tiempo.net
  - url: [https://www.el-tiempo.net/](https://www.el-tiempo.net/api)
2. API2: openweathermap
  - url: [/api.openweathermap.org](https://openweathermap.org/api)
3. API3: open-meteo
  - url: [https://open-meteo.com/en/docs](https://open-meteo.com/en/docs)

## 🎮 Raspi commands

### Raspi ssh access
```
ssh pi@192.168.0.41
```

### Copy files from PC to Raspi
```
scp /Users/imanolpadillo/Documents/weather4cast/*.* pi@192.168.0.41:/home/pi/Documents/weather4cast
````

### Execute weather4cast manually from Raspi
```
cd /home/pi/Documents/weather4cast
python3 main.py
```

### Program a cron for executing weather4cast on restart and delete logs every week
```
sudo crontab -e -u pi
@reboot sh /home/pi/Documents/weather4cast/launcher.sh >/home/pi/Documents/weather4cast/logs/cron.log 2>&1
0 0 * * 0 /bin/rm -f /home/pi/Documents/weather4cast/logs/*
```

### Read Raspi logs
```
cd /home/pi/Documents/weather4cast/logs
cat weather4cast.log
```

### SECRETS
For those APIs that requires an api-key it is necessary to include in parent path a 'secrets.ini' including the following info:
```
[secrets]
api2_key = XXXXXX
```

