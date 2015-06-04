#!/usr/bin/python
import sys
import urllib.request
import json

def getWeatherData(city, units="standard"):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=" + units
    weather = urllib.request.urlopen(url).read()
    return weather

def weatherToJson(weather):
    weatherString = weather.decode("utf-8")
    weatherJson = json.loads(weatherString)
    return weatherJson

def printTemp(data, units):
    temp = data['main']['temp']
    if units == "standard":
        unit = "Kelvin degrees"
    elif units == "metric":
        unit = "Celsius degrees"
    elif units == "imperial":
        unit = "Fahrenheit degrees"

    print(str(temp) + " " + unit)
    return

def help():
    print("First argument: City name, e.g. Cairo,EG")
    print("Second optional argument: [standard, metric, imperial]")

if len(sys.argv) < 2 or len(sys.argv) > 3:
    help()
else:
    city = str(sys.argv[1])
    
    if len(sys.argv) == 3:
        units = str(sys.argv[2])
    else:
        units = "standard"
        
    weather = getWeatherData(city, units)
    weather = weatherToJson(weather)
    printTemp(weather, units)
