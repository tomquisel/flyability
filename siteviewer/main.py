import datetime as dt, pytz
import bisect
from django.http import Http404 
from weather.timeseries import TimeSeries
from weather.models import WeatherSummary
import weather.main as weather
import predictor
import json
from siteviewer.models import Site
import mapstate
from siteviewer.daytime import DayTime

#######################################################################

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

#######################################################################

def getOr404(d, s):
    res = d.get(s)
    if res is None:
        raise Http404
    return res

#######################################################################

def addSiteDetails(site, level):
    setattr(site, 'statecode', mapstate.getCode(site.state))
    try:
        mgr = ForecastMgr(site, level)
        days = mgr.getDays(False)
        setattr(site, 'days', days)
    except weather.NoWeatherDataException: 
        setattr(site, 'days', [])

#######################################################################

def addSummary(site, level):
    summaries = WeatherSummary.objects.filter(site=site, level=level)
    if len(summaries) == 0:
        return
    days = summaries[0].getData()
    out = []
    for day in days:
        obj = {}
        obj['color'] = ForecastMgr.getColor(day['score'])
        obj['short'] = ForecastMgr.shortDay(day['date'])
        out.append(obj)
    out = out[:7]
    setattr(site, 'days', out)
    setattr(site, 'statecode', mapstate.getCode(site.state))

#######################################################################

def addLevels(request, env):
    level = request.session.get('level', 'P2')
    lDicts = []
    for l in predictor.levels:
        lDict = { 'level' : l }
        if level == l:
            lDict['selected'] = True
        lDicts.append(lDict)
    env['levels'] = lDicts
    env['level'] = level

def setLevel(request, level):
    if level in predictor.levels:
        request.session['level'] = level

#######################################################################

class ForecastMgr(object):
    def __init__(self, site, level, startDay = None, days=7):
        self.site = site
        self.level = level
        self.days = days
        self.tz = pytz.timezone(site.timezone)
        if startDay is None:
            now = dt.datetime.now(self.tz)
            startDay = dt.date(now.year, now.month, now.day)
        self.startDay = startDay
        self.startTime = dt.datetime.combine(self.startDay, 
                                             dt.time(tzinfo=self.tz))

        (times, seriesDict, fetchTime) = \
                self.fetchSeries(start = self.startTime, hours = self.days * 24)

        self.times = times
        self.seriesDict = seriesDict
        self.fetchTime = fetchTime
        self.dayTime = DayTime(site, times)

    def getDay(self, start):
        end = start + dt.timedelta(days=1)
        i = bisect.bisect_left(self.times, start)
        startInd = None
        endInd = None
        while i < len(self.times) and self.times[i] < end:
            isDay = self.dayTime.isDay(self.times[i]) 
            if isDay and startInd is None:
                startInd = i
            if not isDay and not startInd is None:
                endInd = i
                break
            i += 1
        times = self.times[startInd:endInd]
        names = ['flyability', 'dir', 'wind', 'gust', 'pop']
        values = {}
        for n in names:
            fullName = self.level + "_" + n
            if fullName in self.seriesDict:
                vals = self.seriesDict[fullName].\
                    interpolate(self.times[startInd:endInd])
            else:
                vals = [0] * (endInd - startInd)
            values[n] = vals
        return (predictor.summarizeScores(scores), times, values)

    @classmethod
    def shortDay(cls, d):
        dow = d.strftime("%w")
        return ['Su','M', 'T', 'W', 'Th', 'F', 'Sa'][int(dow)]

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
            day['short'] = self.shortDay(dayStart)
            day['date'] = dayStart
            fly, flyTimes, flyValues = self.getDay(dayStart)
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

    def computeHighlightDay(self, days):
        day = 1
        bestScore = 1
        for i,d in enumerate(days):
            if i == 0:
                continue
            score = d['flyability'] * 1.0 / (i+1)
            if score > bestScore:
                day = i
                bestScore = score
        return days[day]['name']

    def getValues(self, name, times):
        return self.seriesDict[name].interpolate(times)

    def getValue(self, name, time):
        return self.seriesDict[name].interpolate([time])[0]

    def fetchSeries(self, start=dt.datetime.now(), hours=168):
        wdata = weather.getWeatherData(self.site, start)
        times = TimeSeries.range(start, hours, TimeSeries.hour)
        awareTimes = TimeSeries.makeAware(times, self.tz)
        return (times, wdata.seriesDict, wdata.fetchTime)
