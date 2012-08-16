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
    dayNames = [ d.strftime("%A") for d in days]
    env = {'site' : site, 'days': dayNames}
    return render_to_response('siteviewer/siteview.html', env,
                              context_instance=RequestContext(request))

def forecastImage(request, name):
    site = get_object_or_404(Site, pk=name)
    (times, seriesDict) = main.getForecast(site)
    canvas = grapher.plot(times, seriesDict, canvas = True)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.clf()
    return response
