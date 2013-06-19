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
            dirProb, windProb, gustProb, popProb, prob = \
                getSinglePrediction(dir[i], wind[i], gust[i], pop[i],
                    self.maxWind, self.maxGust, site)
            if not self.dayTime.isDay(t):
                prob = 0.0
            values['dir'].append(dirProb)
            values['wind'].append(windProb)
            values['gust'].append(gustProb)
            values['pop'].append(popProb)
            values['flyability'].append(prob)
        return values


################## HELPERS ##########################

def getSinglePrediction(dir, wind, gust, pop, maxWind, maxGust, site):
    def percify(x):
        return int(round(100*x))
    dirProb = getWindDirChances(site, dir)
    windProb = getWindSpeedChances(maxWind, wind)
    gustProb = getWindSpeedChances(maxGust, gust)
    popProb = getRainChances(pop)
    prob = dirProb * windProb * gustProb * popProb
    probs = (dirProb, windProb, gustProb, popProb, prob)
    return map(probs, percify)

def summarizeScores(scores):
    s = list(scores)
    s.sort()
    # take the top 33rd percentile as the score
    summary = s[len(s) * 2 / 3]
    return summary

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

def getWindSpeedChances(maxWind, speed):
    return normSmooth(maxWind-speed, 3)

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

