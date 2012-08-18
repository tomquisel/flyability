import datetime as dt, pytz
from weather.timeseries import TimeSeries
import weather.main as weather
from predictor import Predictor

class ForecastMgr(object):
    def __init__(self, site, days=7):
        self.site = site
        self.days = 7
        self.tz = pytz.timezone(site.timezone)
        self.startDay = dt.date.today()
        self.startTime = dt.datetime.combine(self.startDay, 
                                             dt.time(tzinfo=self.tz))

        (times, seriesDict, predictor) = self.fetchSeries()
        self.times = times
        self.seriesDict = seriesDict
        self.predictor = predictor

    def getDays(self):
        inc = dt.timedelta(days=1)
        days = []
        for n in range(0, self.days):
            day = {}
            dayStart = self.startTime + inc * n
            day['start'] = dayStart
            day['name'] = day['start'].strftime("%A") 
            day['flyability'] = self.predictor.\
                getRangeFlyability(dayStart, dayStart + inc)
            days.append(day)
        return days

    def getSeries(self):
        return (self.times, self.seriesDict)

    def fetchSeries(self):
        return self.fetchForecast(self.startTime)

    def fetchForecast(self, start=dt.datetime.now(), hours=168):
        seriesDict = weather.getWeatherData(self.site)
        times = TimeSeries.range(start, hours, TimeSeries.hour)
        awareTimes = TimeSeries.makeAware(times, self.tz)
        predictor = Predictor(awareTimes, seriesDict, self.site)
        seriesDict['flyability'] = predictor.flyability
        return (times, seriesDict, predictor)

