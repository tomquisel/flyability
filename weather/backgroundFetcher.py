import datetime

import django.utils.timezone as tz
from siteviewer.models import Site
import weather.main
from weather.models import Forecast

sites = Site.objects.all()
old = tz.now() - datetime.timedelta(minutes=30)
for site in sites:
    recent = Forecast.objects.filter(fetchTime__gt=old)
    if len(recent) > 0:
        print "Skipping update of forecast for %s" % site
        continue
    print "Updating forecast for %s" % site
    res = weather.main.fetchForecast(site)
    if res is None:
        print "weather.gov is having trouble. Rejecting results."
        continue
    forecast, values = res
    forecast.save()
    for v in values:
        v.forecast = forecast
        v.save()

