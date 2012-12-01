import pytz, datetime, time
import forecast_parser as fparser
import forecast_fetcher as fetcher
from timeseries import TimeSeries
from weather.models import Forecast, ForecastValue
from weather.models import Observation, ObservationValue
from siteviewer.models import Site
import email.utils

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
    return forecast, values

def isValid(values):
    return True

class NoWeatherDataException(Exception):
    pass

def getWeatherData(site, start):
    forecasts = Forecast.objects.filter(site=site).order_by('-fetch_time')
    if len(forecasts) == 0:
        raise NoWeatherDataException
    # the most recently fetched forecast for this site
    forecast = forecasts[0]

    et = pytz.timezone("US/Eastern")
    fft = et.normalize(forecast.fetch_time.astimezone(et))
    print "Forecast fetch time:", fft
    query = ForecastValue.objects.filter(forecast=forecast)
    values = query.order_by('name','time')
    seriesDict = modelsToTimeSeries(values, site.timezone)

    # get observation data
    observations = Observation.objects.filter(
            site=site
        ).filter(
            time__gt=start
        ).order_by(
            '-fetch_time'
        )
    for o in observations:
        values = ObservationValue.objects.filter(observation=o)
        for v in values:
            if v.name not in seriesDict:
                ts = TimeSeries(v.name, [], [], site.timezone)
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
    validateSeries(seriesDict)
    # do some unit conversions
    TSKnotsToMPH(seriesDict['gust'])
    return seriesDict

def validateSeries(seriesDict):
    names = ['pop', 'wind', 'gust', 'dir']
    for name in names:
        if name not in seriesDict:
            raise NoWeatherDataException

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

def grabTime(s):
    tup = email.utils.parsedate_tz(s)
    ts = email.utils.mktime_tz(tup)
    return ts

if __name__ == "__main__":
    debug()
