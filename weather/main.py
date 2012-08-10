import xml2models
import fetcher
from weather.models import Forecast, ForecastValue, Scale, TimeSeries

def fetchForecast(site):
    hourly = fetcher.cachingFetch(fetcher.hourlyWeather, (site.lat, site.lon))
    #fourhourly = cachingFetch(fourHourlyWeather, (lat, lon))
    forecast, values = xml2models.parseHourlyData(hourly, site)
    return forecast, values

def getWeatherData(site):
    # the most recently fetched forecast
    forecast = Forecast.objects.order_by('-fetchTime')[0]
    query = ForecastValue.objects.filter(forecast=forecast.id)
    values = query.order_by('name','time').values('name','time','value')
    return modelsToTimeSeries(values)

#def modelsToTimeSeries(values):
#    s = Scale()
#    series = {}
#    for v in values:
#        arrays.get(v['name'], TimeSeries()append(
