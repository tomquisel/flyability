from xml2json import Xml2TimeSeries, Scale, TimeSeries
import grapher

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

def graphData(scale, timeseries, flyability, canvas = False):
    #start = 0
    #for t in scale.times:
    #    if t.hour==0:
    #        break
    #    start += 1

    #end = start + 48
    start = 0
    end = len(scale.times)

    for x in timeseries:
        x.values = x.values[start:end]

    return grapher.plot(scale.times[start:end], timeseries, flyability, canvas = canvas)
