#!/usr/bin/python
import sys
import urllib.request
import json

def getWeatherData(city, units="standard"):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=" + units
    weather = urllib.request.urlopen(url).read()
    weatherString = weather.decode("utf-8")
    weatherJson = json.loads(weatherString)
    return weatherJson

def printTemp(data, units):
    if data['cod'] == "404":
        print("City not found.")
        return

    if units == "standard":
        unitString = "°K"
    elif units == "metric":
        unitString = "°C"
    elif units == "imperial":
        unitString = "°F"

    temp = data['main']['temp']
    humidity = data['main']['humidity']

    print("Temperature: " + str(int(temp)) + unitString)
    print("Humidity: " + str(humidity) + "%")
    return

def help():
    print("First mandatory argument: City name, e.g. Cairo,EG or Helsinki")
    print("Second optional argument: [s]tandard, [m]etric, [i]mperial")
    sys.exit(-1)

if len(sys.argv) < 2 or len(sys.argv) > 3:
    help()
else:
    city = str(sys.argv[1])
    
    units = "metric"
    if len(sys.argv) == 3:
        if sys.argv[2].startswith("s"):
            units = "standard";
        elif sys.argv[2].startswith("i"):
            units = "imperial"
        
    weather = getWeatherData(city, units)
    printTemp(weather, units)
