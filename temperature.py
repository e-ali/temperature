#!/usr/bin/python
import getopt
import json
import os
import time
import sys
import urllib.request

def help():
    print("Name: Eslam's temperature script, using openweathermap.org")
    print("Synopsis: temperature.py [ -m|-i|-s ] [ -c CITY ] [ -d -o ]")
    print("Options:")
    print("\t-m: Metric units, -i: Imperial units, -s: Kelvin")
    print("\t-c: City name, e.g. Cairo, Helsinki")
    print("\t-d: Daemonize, see -f")
    print("\t-f: Filename to output the weather data to, see -d")

def getWeatherData(city, units="standard"):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=" + units
    url += "&APPID=019c6096c37a2e9a4561ac67304a2846"
    weather = urllib.request.urlopen(url).read()
    weather = weather.decode("utf-8")
    return json.loads(weather)

def weatherString(data, units):
    if data['cod'] == "404":
        return "City not found."

    if units == "standard":
        unitString = "°K"
    elif units == "metric":
        unitString = "°C"
    elif units == "imperial":
        unitString = "°F"

    temp = data['main']['temp']
    humidity = data['main']['humidity']
    city = data['name']

    weather = city + "'s temperature: " + str(int(temp)) + unitString
    weather += " | Humidity: " + str(humidity) + "%"
    return weather

def daemonize(city, units, forecast_file):
    while True:
        weather = getWeatherData(city, units)
        forecast = weatherString(weather, units)
        try:
            f = open(forecast_file, 'w')
        except IOError:
            print("Unable to open the file: " + forecast_file)
            sys.exit(2)
        if forecast:
            f.write(forecast)
            f.close()
        time.sleep(10*60)
    return

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:smido:", ["city=", "out="])
    except getopt.GetoptError as err:
        help()
        sys.exit(2)
    units = "metric"
    daemon = False
    city = False
    forecast_file = "/tmp/forecast_" + str(os.getpid())
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
        elif o == "-o" or o == "--output":
            forecast_file = a;
        else:
            assert False, "unhandled option"

    if not city:
        help()
        sys.exit(2)

    if daemon:
        if not forecast_file:
            print("No output file specified")
            sys.exit(2)
        else:
            daemonize(city, units, forecast_file);
    else:
        weather = getWeatherData(city, units)
        weather = weatherString(weather, units)
        print(weather)
    return

if __name__ == "__main__":
    main()
