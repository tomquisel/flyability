import datetime as dt, pytz
from django.http import Http404 
from weather.timeseries import TimeSeries
import weather.main as weather
from predictor import Predictor
import json
from siteviewer.models import Site
import mapstate

def getAllSites():
    query = Site.objects.filter(
                country = "United States"
            ).exclude(
                    takeoffObj = '[[0, 360, "no"]]'
            ).exclude(
                website = ""       
            ).exclude(
                name__contains = "PPG"
            ).exclude(
                name__contains = "no PG"
            )
    sites = list(query)
    return sites

def getOr404(d, s):
    res = d.get(s)
    if res is None:
        raise Http404
    return res

def addSiteDetails(site):
    setattr(site, 'statecode', mapstate.getCode(site.state))
    try:
        mgr = ForecastMgr(site)
        days = mgr.getDays(False)
        setattr(site, 'days', days)
    except weather.NoWeatherDataException: 
        setattr(site, 'days', [])


class ForecastMgr(object):
    def __init__(self, site, startDay = None, days=7):
        self.site = site
        self.days = days
        self.tz = pytz.timezone(site.timezone)
        if startDay is None:
            now = dt.datetime.now(self.tz)
            startDay = dt.date(now.year, now.month, now.day)
        self.startDay = startDay
        self.startTime = dt.datetime.combine(self.startDay, 
                                             dt.time(tzinfo=self.tz))

        (times, seriesDict, predictor, fetchTime) = \
                self.fetchSeries(start = self.startTime, hours = self.days * 24)

        self.times = times
        self.seriesDict = seriesDict
        self.predictor = predictor
        self.fetchTime = fetchTime

    @classmethod
    def shortDay(cls, i):
        return ['Su','M', 'T', 'W', 'Th', 'F', 'Sa'][int(i)]

    @classmethod 
    def interpolateColor(cls, start, end, magnitude):
        res = []
        for i in range(len(start)):
            s = start[i]
            e = end[i]
            col = s + (e-s) * magnitude
            res.append(int(col))
        return tuple(res)

    @classmethod
    def getColor(cls, fly):
        magnitude = fly / 100.0
        s = "rgb(%s,%s,%s)"
        start = (230, 230, 230)
        end = (78, 165, 78)
        color = cls.interpolateColor(start, end, magnitude)
        return s % color


    def getDays(self, includeHours=True):
        inc = dt.timedelta(days=1)
        days = []
        for n in range(0, self.days):
            day = {}
            dayStart = self.startTime + inc * n
            day['start'] = dayStart
            day['name'] = dayStart.strftime("%A") 
            day['short'] = self.shortDay(dayStart.strftime("%w"))
            day['date'] = dayStart
            fly, flyTimes, flyValues = self.predictor.getDay(dayStart)
            day['flyability'] = fly
            # horrible that this isn't in the template 
            day['barheight'] = int(round(44 * fly / 100))
            day['color'] = self.getColor(fly)
            day['hours'] = []
            names = ['wind', 'gust', 'dir', 'pop', 'clouds', 'temp']
            if includeHours:
                for i,t in enumerate(flyTimes):
                    hour = {}
                    hour['name'] = t.strftime("%l %P").strip()
                    hour['hour'] = t.hour
                    hour['flyability'] = flyValues['flyability'][i]
                    for name in names:
                        hour[name] = self.getValue(name, t)
                    day['hours'].append(hour)
                for name in names:
                    vals = self.getValues(name, flyTimes)
                    vals = TimeSeries.stripTrailingNones(vals)
                    day[name] = TimeSeries.substitute(vals, None, 0.0)
                day['scores'] = flyValues['flyability']
                day['flyDetails'] = json.dumps(flyValues)
                day['times'] = json.dumps([ h['name'] for h in day['hours'] ])
            days.append(day)
        return days

    def getValues(self, name, times):
        return self.seriesDict[name].interpolate(times)

    def getValue(self, name, time):
        return self.seriesDict[name].interpolate([time])[0]

    def fetchSeries(self, start=dt.datetime.now(), hours=168):
        wdata = weather.getWeatherData(self.site, start)
        times = TimeSeries.range(start, hours, TimeSeries.hour)
        awareTimes = TimeSeries.makeAware(times, self.tz)
        predictor = Predictor(awareTimes, wdata.seriesDict, self.site)
        return (times, wdata.seriesDict, predictor, wdata.fetchTime)
