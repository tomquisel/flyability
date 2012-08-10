import main
from siteviewer.models import Site
from weather.models import Forecast
import django.utils.timezone as tz
import datetime

sites = Site.objects.all()
old = tz.now() - datetime.timedelta(minutes=30)
for site in sites:
    recent = Forecast.objects.filter(fetchTime__gt=old)
    if len(recent) > 0:
        print "Skipping update of forecast for %s" % site
        continue
    print "Updating forecast for %s" % site
    forecast, values = main.fetchForecast(site)
    forecast.save()
    for v in values:
        v.forecast = forecast
        v.save()

