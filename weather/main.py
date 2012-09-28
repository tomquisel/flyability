import pytz, datetime
import forecast_parser as fparser
import forecast_fetcher as fetcher
from timeseries import TimeSeries
from weather.models import Forecast, ForecastValue
from weather.models import Observation, ObservationValue
from siteviewer.models import Site

def fetchForecast(site):
    forecast = Forecast(site = site, lat = site.lat, lon = site.lon)
    hourly = fetcher.cachingFetch(fetcher.hourlyWeather, (site.lat, site.lon))
    values = fparser.parseHourlyData(hourly)
    fourhourly = fetcher.cachingFetch(fetcher.fourHourlyWeather, 
                                      (site.lat, site.lon))
    fourvalues = fparser.parseFourHourlyData(fourhourly)
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

def getWeatherData(site, start):
    # the most recently fetched forecast for this site
    forecast = Forecast.objects.filter(site=site).order_by('-fetch_time')[0]
    et = pytz.timezone("US/Eastern")
    fft = et.normalize(forecast.fetch_time.astimezone(et))
    print "Forecast fetch time:", fft
    query = ForecastValue.objects.filter(forecast=forecast)
    values = query.order_by('name','time')
    seriesDict = modelsToTimeSeries(values, site.timezone)

    # get observation data
    observations = Observation.objects.filter(
            time__gt=start
        ).order_by(
            '-fetch_time'
        )
    for o in observations:
        values = ObservationValue.objects.filter(observation=o)
        for v in values:
            seriesDict[v.name].add(o.time, v.value)

    return seriesDict

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
