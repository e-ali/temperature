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
    print("Second optional argument: [standard, metric, imperial]")

if len(sys.argv) < 2 or len(sys.argv) > 3:
    help()
else:
    city = str(sys.argv[1])
    
    if len(sys.argv) == 3:
        units = str(sys.argv[2])
    else:
        units = "metric"
        
    weather = getWeatherData(city, units)
    weather = weatherToJson(weather)
    printTemp(weather, units)
