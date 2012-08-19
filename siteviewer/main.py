import datetime as dt, pytz
from weather.timeseries import TimeSeries
import weather.main as weather
from predictor import Predictor

class ForecastMgr(object):
    def __init__(self, site, startDay = dt.date.today(), days=7):
        self.site = site
        self.days = days
        self.tz = pytz.timezone(site.timezone)
        self.startDay = startDay
        self.startTime = dt.datetime.combine(self.startDay, 
                                             dt.time(tzinfo=self.tz))

        (times, seriesDict, predictor) = \
                self.fetchSeries(start = self.startTime, hours = self.days * 24)
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
            day['name'] = dayStart.strftime("%A") 
            day['date'] = dayStart.strftime("%Y-%m-%d") 
            flyabilityHours, flyability = self.predictor.getDay(dayStart)
            day['flyability'] = flyability
            day['hours'] = []
            names = ['wind', 'gust', 'dir', 'pop', 'clouds', 'temp']
            for i,t in enumerate(flyabilityHours.times):
                hour = {}
                hour['name'] = t.strftime("%l%P")
                hour['hour'] = t.hour
                hour['flyability'] = flyabilityHours.values[i]
                for name in names:
                    hour[name] = self.getValue(name, t)
                day['hours'].append(hour)
            for name in names:
                day[name] = self.getValues(name, flyabilityHours.times)
            day['scores'] = flyabilityHours.values
            days.append(day)
        return days

    def getSeries(self):
        return (self.times, self.seriesDict)

    def getValues(self, name, times):
        return self.seriesDict[name].read(times, 0)

    def getValue(self, name, time):
        return self.seriesDict[name].read([time], 0)[0]

    def fetchSeries(self, start=dt.datetime.now(), hours=168):
        seriesDict = weather.getWeatherData(self.site)
        times = TimeSeries.range(start, hours, TimeSeries.hour)
        awareTimes = TimeSeries.makeAware(times, self.tz)
        predictor = Predictor(awareTimes, seriesDict, self.site)
        seriesDict['flyability'] = predictor.flyability
        return (times, seriesDict, predictor)

