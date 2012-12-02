import astral
import datetime
from scipy.stats import norm
from weather.timeseries import TimeSeries
import bisect
import numpy as np

class Predictor(object):

    def __init__(self, times, timeseries, site):
        self.times = times
        self.timeseries = timeseries
        self.site = site

        self.dayIntervals = self.getDayIntervals()
        self.values = self.computeFlyability()
        self.flyability = TimeSeries("flyability", self.times, self.values, 
                                     self.site.timezone)

    def getDay(self, start):
        end = start + datetime.timedelta(days=1)
        i = bisect.bisect_left(self.times, start)
        startInd = None
        endInd = None
        while i < len(self.times) and self.times[i] < end:
            isDay = self.isDay(self.times[i]) 
            if isDay and startInd is None:
                startInd = i
            if not isDay and not startInd is None:
                endInd = i
                break
            i += 1
        res = TimeSeries("flyability", self.times[startInd:endInd],
                         self.values[startInd:endInd],
                         self.site.timezone)
        scores = list(res.values)
        scores.sort()
        # take the top 30th percentile as the score
        summary = scores[len(scores) * 2 / 3]
        return (res, summary)

    def computeFlyability(self):
        times = self.times
        timeseries = self.timeseries
        site = self.site
        pop = timeseries['pop'].interpolate(times, 0.0)
        wind = timeseries['wind'].interpolate(times, 0.0)
        dir = timeseries['dir'].interpolate(times, 0.0)

        values = []
        for i,t in enumerate(times):
            prob = 0
            if self.isDay(t):
                prob = 1.0
            prob *= getWindDirChances(site, dir[i])
            prob *= getWindSpeedChances(wind[i])
            prob *= getRainChances(pop[i])
            values.append(100 * prob)

        return values

    def getDayIntervals(self):
        site = self.site
        times = self.times
        days = []
        a = astral.Astral()
        dates = set([])
        for dt in times:
           date = datetime.datetime.date(dt)
           dates.add(date)
        dates = list(dates)
        dates.sort()
        for date in dates:
            sunInfo = a.sun_utc(date, site.lat, site.lon)
            days.append( (sunInfo['sunrise'], sunInfo['sunset']) )
        return days

    def isDay(self, t):
        sunsetFudge = datetime.timedelta(hours=1)
        sunriseFudge = datetime.timedelta(hours=2)
        for sunrise, sunset in self.dayIntervals:
            if t > sunrise + sunriseFudge and t < sunset + sunsetFudge:
                return True
        return False

################## HELPERS ##########################

class Smoother(object):
    def __init__(self, sd, n, inc):
        self.xs = np.linspace(-n*inc, n*inc, 2*n+1)
        self.weights = norm.pdf(self.xs, scale = sd)

    def smooth(self, vals):
        return np.average(vals, weights=self.weights)

smoothSD = 20
smoothN = 5
smoothInc = 6

smoother = Smoother(smoothSD, smoothN, smoothInc)

def getWindDirChances(site, dir):
    takeoff = site.getTakeoffObj()
    samples = getSamples(dir, takeoff, smoothN, smoothInc)
    res = smoother.smooth(samples)
    #print dir, takeoff
    #print res, samples
    return res

def getWindSpeedChances(speed):
    return normSmooth(12-speed, 1)

def getRainChances(pop):
    return 1 - pop/100.0

def getTakeoffScore(dir, takeoff):
    if dir < 0:
        dir += 360
    if dir >= 360: 
        dir -= 360
    for left,right,good in takeoff:
        if left <= dir <= right:
            return getScore(good)

def getSamples(dir, takeoff, n, inc):
    samples = []
    points = computeSamplePoints(dir, n, inc)
    takeoffScores = np.vectorize(lambda x: getTakeoffScore(x, takeoff))
    scores = takeoffScores(points)
    return scores

def computeSamplePoints(dir, n, inc):
    start = dir - n*inc
    end = dir + n*inc
    points = np.linspace(start, end, 2*n + 1)
    return points

def getScore(good):
    return {'yes' : 1.0, 'maybe' : 0.65, 'no' : 0.0}[good]

def isInRange(dir, takeoff):
    for left,right,good in takeoff:
        if left <= dir <= right:
            return good == "yes"

def boundaryDist(dir, takeoff):
    dist = 360
    for left,right,good in takeoff:
        if good == "yes":
            dl = abs(dir-left)
            dr = abs(dir-right)
            if dl < dist:
                dist = dl
            if dr < dist:
                dist = dr
    return dist

# negative values are worse than 50%, positive are better
def normSmooth(val, sd):
    return norm.cdf(val, scale = sd)

