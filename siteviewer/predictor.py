from xml2json import Scale, TimeSeries
import astral
import datetime
from scipy.stats import norm

def flyability(site, times, timeseries):
    temp, dewpt, pop, wind, dir, clouds, humidity = timeseries
    res = TimeSeries("flyability")

    dayIntervals = getDayIntervals(site, times)

    for i,t in enumerate(times.awareTimes):
        prob = 0
        if isDay(t, dayIntervals):
            prob = 1.0
        prob *= getWindDirChances(site, dir.values[i])
        prob *= getWindSpeedChances(wind.values[i])
        prob *= getRainChances(pop.values[i])
        res.values.append(100 * prob)
    return res

################## HELPERS ##########################

def getDayIntervals(site, times):
    days = []
    a = astral.Astral()
    dates = set([])
    for dt in times.awareTimes:
       date = datetime.datetime.date(dt)
       dates.add(date)
    dates = list(dates)
    dates.sort()
    for date in dates:
        sunInfo = a.sun_utc(date, site.lat, site.lon)
        days.append( (sunInfo['sunrise'], sunInfo['sunset']) )
    return days

def isDay(t, dayIntervals, twilightLen = 1):
    twiLen = datetime.timedelta(hours=twilightLen)
    for sunrise, sunset in dayIntervals:
        if t > sunrise + twiLen and t < sunset - twiLen:
            return True
    return False

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
