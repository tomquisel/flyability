import xml2models
import fetcher

def getWeatherData(site):
    hourly = fetcher.cachingFetch(fetcher.hourlyWeather, (site.lat, site.lon))
    #fourhourly = cachingFetch(fourHourlyWeather, (lat, lon))
    forecast, values = xml2models.parseHourlyData(hourly, site)
    return forecast, values
