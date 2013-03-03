import sys
import datetime as dt, pytz
import weather.main as main
from siteviewer.models import Site

name = sys.argv[1]

sites = Site.objects.filter(name=name)
site = sites[0]
tz = pytz.timezone(site.timezone)
start = tz.localize(dt.datetime.now() - dt.timedelta(days=7))
data = main.getWeatherData(site, start)
print data.fetchTime
print data.seriesDict.keys()
for k in data.seriesDict:
    print k
    print data.seriesDict[k].values
