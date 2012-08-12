import pytz
import xml2models
import fetcher
from weather.models import Forecast, ForecastValue, Scale, TimeSeries

def fetchForecast(site):
    forecast = Forecast(site = site, lat = site.lat, lon = site.lon)
    hourly = fetcher.cachingFetch(fetcher.hourlyWeather, (site.lat, site.lon))
    values = xml2models.parseHourlyData(hourly)
    fourhourly = fetcher.cachingFetch(fetcher.fourHourlyWeather, 
                                      (site.lat, site.lon))
    fourvalues = xml2models.parseFourHourlyData(fourhourly)
    values.extend(fourvalues)
    for v in values:
        v.forecast = forecast
    return forecast, values

def getWeatherData(site):
    # the most recently fetched forecast
    forecast = Forecast.objects.order_by('-fetchTime')[0]
    print "Fetch time:", forecast.fetchTime
    query = ForecastValue.objects.filter(forecast=forecast.id)
    values = query.order_by('name','time').values('name','time','value')
    return modelsToTimeSeries(values, pytz.timezone(site.timezone))

def modelsToTimeSeries(values, tz):
    s = Scale()
    series = {}
    timeSet = set([])
    for v in values:
        n = v['name']
        series[n] = series.get(n, TimeSeries(n)).appendValue(v['value'])
        timeSet.add(v['time'])
    ts = list(timeSet)
    ts.sort()
    s.awareTimes = [ tz.normalize(t.astimezone(tz)) for t in ts]
    s.times = [ t.replace(tzinfo=None) for t in s.awareTimes ]

    return (s, series)
