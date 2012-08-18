import astral
import datetime
from scipy.stats import norm
from weather.timeseries import TimeSeries
import bisect

class Predictor(object):

    def __init__(self, times, timeseries, site):
        self.times = times
        self.timeseries = timeseries
        self.site = site

        self.dayIntervals = self.getDayIntervals()
        self.values = self.computeFlyability()
        self.flyability = TimeSeries("flyability", self.times, self.values, 
                                     self.site.timezone)

    def getRangeFlyability(self, start, end):
        i = bisect.bisect_left(self.times, start)
        scores = []
        while i < len(self.times) and self.times[i] < end:
            if self.isDay(self.times[i]):
                scores.append(self.values[i])
            i += 1
        scores.sort()
        # take the top 30th percentile as the score
        res = scores[len(scores) * 2 / 3]
        return res

    def computeFlyability(self):
        times = self.times
        timeseries = self.timeseries
        site = self.site
        pop = timeseries['pop'].read(times, 0.0)
        wind = timeseries['wind'].read(times, 0.0)
        dir = timeseries['dir'].read(times, 0.0)

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

    def isDay(self, t, twilightLen = 1):
        twiLen = datetime.timedelta(hours=twilightLen)
        for sunrise, sunset in self.dayIntervals:
            if t > sunrise + twiLen and t < sunset - twiLen:
                return True
        return False

################## HELPERS ##########################


def getWindDirChances(site, dir):
    left, right = site.getTakeoffRange()
    inRange = isInRange(dir, left, right)
    dist = boundaryDist(dir, left, right)
    diff = dist
    if not inRange:
        diff = -dist
    prob = normSmooth(diff, 15)
    return prob

def getWindSpeedChances(speed):
    return normSmooth(12-speed, 1)

def getRainChances(pop):
    return 1 - pop/100.0

def isInRange(dir, left, right):
    if left < right:
        return left <= dir <= right
    else:
        return dir >= left or dir <= right

def boundaryDist(dir, left, right):
    # fixup broken ranges
    if left > right:
        if dir < right:
            dir += 360
        right += 360
    return min(abs(dir-left),abs(dir-right))

# negative values are worse than 50%, positive are better
def normSmooth(val, sd):
    return norm.cdf(val, scale = sd)
