import datetime as dt, time

import django.utils.timezone as tz
from siteviewer.models import Site
from siteviewer.main import getAllSites
import weather.main
from weather.models import Forecast, ForecastData, Observation, \
        ObservationData, ForecastValue, WeatherSummary
import observation_fetcher as of
import condition
from optparse import OptionParser
from weather.timeseries import TimeSeries
from siteviewer.predictor import Predictor
import siteviewer.predictor as predictor

old = tz.now() - dt.timedelta(minutes=30)

def updateForecast(site):
    t1 = time.time()
    recent = Forecast.objects.filter(site_id=site.id).\
                filter(fetch_time__gt=old)
    #if len(recent) > 0:
    #    print "Skipping update of forecast for %s" % site.name
    #    return
    t2 = time.time()
    print "Updating forecast for %s" % site.name
    res = weather.main.fetchForecast(site)
    t3 = time.time()
    if res is None:
        print "weather.gov is having trouble. Rejecting results."
        return
    forecast, values = res
    forecast.save()
    t4 = time.time()

    # compute our flyability predictions
    try:
        seriesDict = weather.main.modelsToTimeSeries(values, site.timezone)
    except weather.main.NoWeatherDataException:
        print "No weather data for site %s!! Skipping update." % site.name
        return
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

of.fetch()
observationIndex = of.buildIndex()
conditionMgr = condition.buildConditionMgr()
def updateObservation(site):
    t1 = time.time()
    recent = Observation.objects.filter(site_id=site.id).\
                filter(fetch_time__gt=old)
    if len(recent) > 0:
        print "Skipping update of observation for %s" % site.name
        return
    t2 = time.time()
    nearest = observationIndex.getNearest(site.lat, site.lon)
    t3 = time.time()
    result = nearest.next()
    obs, values = result.toDjangoModels(site, conditionMgr)
    obs.save()
    t4 = time.time()
    data = ObservationData(observation = obs)
    data.setData(values)
    data.save()
    t5 = time.time()
    print "Observation: %s %s %s %s" % ( t2-t1, t3-t2, t4-t3, t5-t4)

parser = OptionParser()
parser.add_option("-s", "--site", dest="site",
                  help="update site with this id", metavar="SITE")
(options, args) = parser.parse_args()

if options.site:
    query = Site.objects.filter(id=options.site)
    sites = list(query)
    old = tz.now()
else: 
    sites = getAllSites()

for site in sites:
    print "Fetching forecast for %s, %s, %s %s" % (site.name, site.state, site.country, site.id)
    updateForecast(site)
    updateObservation(site)
