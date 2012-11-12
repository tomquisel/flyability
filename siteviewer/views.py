import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_control
from siteviewer.models import Site
import siteviewer.main as main
import grapher, multigrapher

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

def distCmp(s1, s2, lat, lon):
    return cmp(dist(s1, lat, lon), dist(s2, lat, lon))

def dist(s, lat, lon):
    return ((s.lat-lat)**2 + (s.lon-lon)**2)**0.5


def search(request):
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    sites = list(Site.objects.all())
    sites.sort(lambda s1, s2: distCmp(s1, s2, lat, lon))
    for s in sites:
        setattr(s, 'dist', dist(s, lat, lon))
    env = { 'sites' : sites[:20] }
    return render_to_response('siteviewer/search.html', env,
                              context_instance=RequestContext(request))

@cache_control(public=True, max_age=3600*24*365)
def windDir(request, wind, left, right, size):
    wind, left, right, size = int(wind), int(left), int(right), int(size)
    showWind = wind >= 0
    response = multigrapher.runGrapher(
            lambda : grapher.drawWindDir(wind, left, right, size, showWind)
    )
    return response

def windArrow(request, wind, left, right, size):
    wind, left, right, size = int(wind), int(left), int(right), int(size)
    response = multigrapher.runGrapher(
            lambda : grapher.drawArrow(wind, left, right, size)
    )
    return response
