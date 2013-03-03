import datetime
from collections import defaultdict
import numpy as np
from scipy.stats import norm
from weather.timeseries import TimeSeries
from siteviewer.daytime import DayTime

levels = [ 'P2', 'P3', 'P4' ]
windMaxMap = { 'P2' : 12, 'P3' : 15, 'P4' : 20 }
gustMaxMap = { 'P2' : 15, 'P3' : 18, 'P4' : 25 }

class Predictor(object):

    def __init__(self, times, timeseries, site, level):
        self.site = site
        self.times = times
        self.timeseries = timeseries
        self.maxWind = windMaxMap[level]
        self.maxGust = gustMaxMap[level]
        self.dayTime = DayTime(site, times)

        self.values = self.computeFlyability()

    def computeFlyability(self):
        times = self.times
        timeseries = self.timeseries
        site = self.site
        pop = timeseries['pop'].interpolate(times, 0.0)
        wind = timeseries['wind'].interpolate(times, 0.0)
        gust = timeseries['gust'].interpolate(times, 0.0)
        dir = timeseries['dir'].interpolate(times, 0.0)

        values = defaultdict(list)
        for i,t in enumerate(times):
            prob = 0
            if self.dayTime.isDay(t):
                prob = 1.0
            dirProb = getWindDirChances(site, dir[i])
            windProb = self.getWindSpeedChances(wind[i])
            gustProb = self.getGustSpeedChances(gust[i])
            popProb = getRainChances(pop[i])
            prob *= dirProb * windProb * gustProb * popProb
            values['dir'].append(int(round(100 * dirProb)))
            values['wind'].append(int(round(100 * windProb)))
            values['gust'].append(int(round(100 * gustProb)))
            values['pop'].append(int(round(100 * popProb)))
            values['flyability'].append(int(round(100 * prob)))

        return values

    def getWindSpeedChances(self, speed):
        return normSmooth(self.maxWind-speed, 3)

    def getGustSpeedChances(self, speed):
        return normSmooth(self.maxGust-speed, 3)


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

