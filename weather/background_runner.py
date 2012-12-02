import datetime, time

import django.utils.timezone as tz
from siteviewer.models import Site
from siteviewer.main import getAllSites
import weather.main
from weather.models import Forecast, ForecastData, Observation, ObservationData
import observation_fetcher as of
import condition
from optparse import OptionParser

old = tz.now() - datetime.timedelta(minutes=30)

def updateForecast(site):
    t1 = time.time()
    recent = Forecast.objects.filter(site_id=site.id).\
                filter(fetch_time__gt=old)
    if len(recent) > 0:
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
    forecast.save()
    t4 = time.time()
    data = ForecastData(forecast=forecast)
    data.setData(values)
    data.save()
    t5 = time.time()
    print "Forecast: %s %s %s %s" % ( t2-t1, t3-t2, t4-t3, t5-t4)

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
