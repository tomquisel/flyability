import datetime as dt
import time
from optparse import OptionParser

import django.utils.timezone as tz

import weather.main
from weather.models import (Forecast, ForecastData, Observation,
        ObservationData, ForecastValue, WeatherSummary)
import observation_fetcher
import condition
from weather.timeseries import TimeSeries
from siteviewer.models import Site
from siteviewer.main import getAllSites
from siteviewer.predictor import Predictor
import siteviewer.predictor as predictor


def main():
    recentCutoff = tz.now() - dt.timedelta(minutes=30)

    parser = OptionParser()
    parser.add_option("-s", "--site", dest="site",
                      help="update site with this id", metavar="SITE")
    (options, args) = parser.parse_args()

    if options.site:
        query = Site.objects.filter(id=options.site)
        sites = list(query)
        recentCutoff = tz.now()
    else: 
        sites = getAllSites()

    observationUpdater = ObservationUpdater(recentCutoff)
    for site in sites:
        print "Fetching forecast & observation for %s, %s, %s %s" % \
                (site.name, site.state, site.country, site.id)
        updateForecast(site, recentCutoff)
        observationUpdater.update(site)


def updateForecast(site, recentCutoff):
    t1 = time.time()
    if recentExistsAlready(Forecast, site, recentCutoff):
        print "Skipping update of forecast for %s" % site.name
        return
    t2 = time.time()
    print "Updating forecast for %s" % site.name
    res = weather.main.fetchForecast(site)
    t3 = time.time()
    if res is None:
        print "weather.gov is having trouble. Rejecting results."
        return
    forecast, values = res
    t4 = time.time()

    # compute our flyability predictions
    try:
        seriesDict = weather.main.modelsToTimeSeries(values, site.timezone)
    except weather.main.NoWeatherDataException:
        print "No weather data for site %s!! Skipping update." % site.name
        return
    # we got data back, we can safely save the forecast without creating
    # a dangling entry
    forecast.save()
    thisHour = dt.datetime.now().replace(minute=0, second=0, microsecond=0)
    times = TimeSeries.range(thisHour, 168, TimeSeries.hour)
    awareTimes = TimeSeries.makeAware(times, seriesDict['wind'].tz)
    for level in predictor.levels:
        pred = Predictor(awareTimes, seriesDict, site, level)
        flyability = pred.computeFlyability()
        #print level
        #print flyability['flyability']
        for name in flyability:
            for i,f in enumerate(flyability[name]):
                fullName = level + "_" + name
                values.append(ForecastValue(fullName, flyability[name][i], 
                              pred.times[i]))
        saveSummaryData(site, level, pred.dayTime, pred.times, \
                flyability['flyability'])
    data = ForecastData(forecast=forecast)
    data.setData(values)
    data.save()


    t5 = time.time()
    print "Forecast: %s %s %s %s" % ( t2-t1, t3-t2, t4-t3, t5-t4)


def saveSummaryData(site, level, dayTime, times, scores):
    summaryData = []
    curScores = []
    curDate = None
    l = len(times)
    for i,f in enumerate(scores):
        isDay = dayTime.isDay(times[i])
        if isDay:
            curScores.append(f)
            curDate = times[i].date()
        if (not isDay and len(curScores)) or (isDay and i == l-1):
            obj = {}
            obj['date'] = curDate
            obj['score'] = predictor.summarizeScores(curScores)
            summaryData.append(obj)
            curScores = []
    assert(len(curScores) == 0)
    WeatherSummary.objects.filter(site=site, level=level).delete()
    summary = WeatherSummary(site=site, level=level)
    #print summaryData
    summary.setData(summaryData)
    summary.save()


class ObservationUpdater(object):
    
    def __init__(self, recentCutoff):
        self.recentCutoff = recentCutoff
        observation_fetcher.fetch()
        self.observationIndex = observation_fetcher.buildIndex()
        self.conditionMgr = condition.buildConditionMgr()

    def update(self, site):
        if recentExistsAlready(Observation, site, self.recentCutoff):
            print "Skipping update of observation for %s" % site.name
            return
        print "Updating observation for %s" % site.name
        nearest = self.observationIndex.getNearest(site.lat, site.lon).next()
        self.saveFullObservation(site, nearest)

    def saveFullObservation(self, site, observation):
        obs, values = observation.toDjangoModels(site, self.conditionMgr)
        obs.save()
        data = ObservationData(observation = obs)
        data.setData(values)
        data.save()


def recentExistsAlready(model, site, recentCutoff):
    recent = model.objects.filter(site_id=site.id, fetch_time__gt=recentCutoff)
    return len(recent) > 0


if __name__ == '__main__':
    main()
