import datetime

import django.utils.timezone as tz
from siteviewer.models import Site
import weather.main
from weather.models import Forecast, Observation
import observation_fetcher as of
import condition

old = tz.now() - datetime.timedelta(minutes=30)

def updateForecast(site):
    recent = Forecast.objects.filter(fetchTime__gt=old)
    if len(recent) > 0:
        print "Skipping update of forecast for %s" % site
        return
    print "Updating forecast for %s" % site
    res = weather.main.fetchForecast(site)
    if res is None:
        print "weather.gov is having trouble. Rejecting results."
        return
    forecast, values = res
    forecast.save()
    for v in values:
        v.forecast = forecast
        v.save()

of.fetch()
observationIndex = of.buildIndex()
conditionMgr = condition.buildConditionMgr()
def updateObservation(site):
    recent = Observation.objects.filter(fetchTime__gt=old)
    if len(recent) > 0:
        print "Skipping update of observation for %s" % site
        return
    nearest = observationIndex.getNearest(site.lat, site.lon)
    result = nearest.next()
    obs, values = result.toDjangoModels(site, conditionMgr)
    obs.save()
    for v in values:
        v.observation = obs
        v.save()

sites = Site.objects.all()
for site in sites:
    updateForecast(site)
    updateObservation(site)
