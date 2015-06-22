#!/usr/bin/python
import getopt
import json
import time
import sys
import urllib.request

def help():
    print("First mandatory argument: City name, e.g. Cairo,EG or Helsinki")
    print("Second optional argument: [s]tandard, [m]etric, [i]mperial")

def getWeatherData(city, units="standard"):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&units=" + units
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

    weather = "Temperature: " + str(int(temp)) + unitString + "\n"
    weather += "Humidity: " + str(humidity) + "%"
    return weather

def daemonize(city, units):
    while True:
        weather = getWeatherData(city, units)
        f = open('forecast', 'w')
        forecast = weatherString(weather, units)
        if forecast:
            f.write(forecast)
            f.close()
        time.sleep(10*60)
    return

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
        else:
            assert False, "unhandled option"

    if not city:
        help()
        sys.exit(2)

    if daemon:
        daemonize(city, units);
    else:
        weather = getWeatherData(city, units)
        weather = weatherString(weather, units)
        print(weather)
    return

if __name__ == "__main__":
    main()
