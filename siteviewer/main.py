import datetime as dt, pytz
from weather.timeseries import TimeSeries
import weather.main as weather
import predictor

class ForecastMgr(object):
    def __init__(self, site, days=7):
        self.site = site
        self.days = 7
        self.todayStart = dt.datetime.combine(dt.date.today(), dt.time())

    def getData(self):
        return getForecast(self.site, self.todayStart)

    def getDays(self):
        today = dt.date.today()
        day = dt.timedelta(days=1)
        return [today + day*n for n in range(0, self.days)]

def getForecast(site, start=dt.datetime.now(), hours=168):
    seriesDict = weather.getWeatherData(site)
    tz = pytz.timezone(site.timezone)
    times = TimeSeries.range(start, hours, TimeSeries.hour)
    awareTimes = TimeSeries.makeAware(times, tz)
    flyability = predictor.flyability(site, awareTimes, seriesDict)
    seriesDict['flyability'] = flyability
    return (times, seriesDict)
