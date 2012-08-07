import fetcher
import converter
from siteviewer.models import Site

sites = Site.objects.all()
for site in sites:
    getWeatherData(site.lat, site.lon)
