from xml2json import Xml2TimeSeries, Scale, TimeSeries
import fetcher

def getWeatherData(lat, lon):
    hourly = cachingFetch(hourlyWeather, (lat, lon))
    fourhourly = cachingFetch(fourHourlyWeather, (lat, lon))

def parseData(data):
    scale = Scale()
    temp = TimeSeries("temperature", type="hourly")
    dewpt = TimeSeries("temperature", type="dew point")
    pop = TimeSeries("probability-of-precipitation")
    wind = TimeSeries("wind-speed", type="sustained")
    dir = TimeSeries("direction")
    clouds = TimeSeries("cloud-amount")
    humidity = TimeSeries("humidity")
    timeseries = [temp, dewpt, pop, wind, dir, clouds, humidity]
    # populates items in place
    Xml2TimeSeries(scale, timeseries, data)
    return (scale, timeseries)
