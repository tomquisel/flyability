import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
import matplotlib.pyplot as plt

from siteviewer.models import Site
import siteviewer.main as main
import grapher

def site(request, name):
    site = get_object_or_404(Site, pk=name)
    mgr = main.ForecastMgr(site)
    days = mgr.getDays()
    env = {'site' : site, 'days': days}
    return render_to_response('siteviewer/siteview.html', env,
                              context_instance=RequestContext(request))

def forecastImage(request, name, date):
    site = get_object_or_404(Site, pk=name)
    start = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    mgr = main.ForecastMgr(site, start, days=1)
    (times, seriesDict) = mgr.getSeries()
    canvas = grapher.plot(times, seriesDict, canvas = True)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.clf()
    return response
