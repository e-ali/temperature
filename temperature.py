#!/usr/bin/python
import getopt
import json
import time
import sys
import urllib.request

def getWeatherData(city, units="standard"):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=" + units
    weather = urllib.request.urlopen(url).read()
    weather = weather.decode("utf-8")
    return json.loads(weather)

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

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:smid", ["city="])
    except getopt.GetoptError as err:
        help()
        sys.exit(2)
    units = "metric"
    daemon = False
    city = False
    for o, a in opts:
        if o == "-s":
            units = "standard";
        elif o == "-m":
            units = "metric";
        elif o == "-i":
            units = "imperial";
        elif o == "-d":
            daemon = True;
        elif o == "-h":
            help()
            sys.exit(0)
        elif o == "-c" or o == "--city":
            city = a;

    if not city:
        help()
        sys.exit(2)

    weather = getWeatherData(city, units)
    printTemp(weather, units)
    return

def daemonize():
    return

if __name__ == "__main__":
    main()
