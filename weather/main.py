import pytz, datetime
import xml2models
import fetcher
from weather.models import Forecast, ForecastValue
from timeseries import TimeSeries
from siteviewer.models import Site

def fetchForecast(site):
    forecast = Forecast(site = site, lat = site.lat, lon = site.lon)
    hourly = fetcher.cachingFetch(fetcher.hourlyWeather, (site.lat, site.lon))
    values = xml2models.parseHourlyData(hourly)
    fourhourly = fetcher.cachingFetch(fetcher.fourHourlyWeather, 
                                      (site.lat, site.lon))
    fourvalues = xml2models.parseFourHourlyData(fourhourly)
    values.extend(fourvalues)
    if not isValid(values):
        return None
    for v in values:
        v.forecast = forecast
    return forecast, values

def isValid(values):
    counts = {}
    for v in values:
        counts[v.name] = counts.get(v.name,0) + 1
    for name,count in counts.items():
        if name == 'gust':
            if count < 18:
                print "Error: %s has %d values" % (name, count)
                return False
        else:
            if count < 166:
                print "Error: %s has %d values" % (name, count)
                return False
    return True

def getWeatherData(site):
    # the most recently fetched forecast
    forecast = Forecast.objects.order_by('-fetchTime')[0]
    et = pytz.timezone("US/Eastern")
    print "Fetch time:", et.normalize(forecast.fetchTime.astimezone(et))
    query = ForecastValue.objects.filter(forecast=forecast.id)
    values = query.order_by('name','time')
    res = modelsToTimeSeries(values, site.timezone)
    return res

def modelsToTimeSeries(values, tz):
    seriesDict = {}
    valuesDict = {}
    for v in values:
        n = v.name
        l = valuesDict.get(n,[])
        l.append(v)
        valuesDict[n] = l
    for n,vlist in valuesDict.items():
        seriesDict[n] = TimeSeries.fromModels(vlist, tz)
    # do some unit conversions
    TSKnotsToMPH(seriesDict['gust'])
    return seriesDict

def TSKnotsToMPH(ts):
    ts.values = [ knotsToMPH(v) for v in ts.values ]

def knotsToMPH(knots):
    return knots * 1.15078

def debug():
    sites = Site.objects.all()
    forecast, values = fetchForecast(sites[0])
    print forecast
    for v in values:
        print v

if __name__ == "__main__":
    debug()
