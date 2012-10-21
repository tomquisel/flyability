import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from siteviewer.models import Site
import siteviewer.main as main
import grapher
import threading

threadLock = threading.Lock()

def index(request):
    env = {}
    return render_to_response('siteviewer/index.html', env,
                              context_instance=RequestContext(request))

def shim(request):
    return site(request, "United States", "New York", "Brace")

def site(request, country, state, name):
    site = get_object_or_404(Site, pk=name)
    left, right = site.getTakeoffRange()
    site.left = left
    site.right = right
    mgr = main.ForecastMgr(site)
    days = mgr.getDays()
    env = {'site' : site, 'days': days}
    return render_to_response('siteviewer/siteview.html', env,
                              context_instance=RequestContext(request))

def state(request, country, state):
    sites = Site.objects.filter(
                             country = country
                         ).filter(
                             state = state
                         )
    env = {'sites' : sites, 'country' : country, 'state' : state}
    return render_to_response('siteviewer/statelist.html', env,
                              context_instance=RequestContext(request))
def country(request, country):
    sites = Site.objects.filter(country = country)
    env = {'sites' : sites, 'country' : country}
    return render_to_response('siteviewer/countrylist.html', env,
                              context_instance=RequestContext(request))

def allSiteNames(request):
    sites = Site.objects.all()
    names = [ "%s, %s, %s" % (s.name, s.state, s.country) for s in sites]
    env = { 'names' : names }
    return render_to_response('siteviewer/api/allsitenames.html', env,
                              context_instance=RequestContext(request))

def windDir(request, wind, left, right, size):
    wind, left, right, size = int(wind), int(left), int(right), int(size)
    showWind = wind >= 0
    threadLock.acquire()
    canvas = grapher.drawWindDir(wind, left, right, size, showWind)
    threadLock.release()
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    grapher.finish()
    return response

def windArrow(request, wind, left, right, size):
    wind, left, right, size = int(wind), int(left), int(right), int(size)
    threadLock.acquire()
    canvas = grapher.drawArrow(wind, left, right, size)
    threadLock.release()
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response, transparent=True)
    grapher.finish()
    return response

def forecastImage(request, name, date):
    site = get_object_or_404(Site, pk=name)
    start = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    mgr = main.ForecastMgr(site, start, days=1)
    (times, seriesDict) = mgr.getSeries()
    canvas = grapher.plot(times, seriesDict, canvas = True)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    grapher.finish()
    return response
