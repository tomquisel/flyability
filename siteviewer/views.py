import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_control
from siteviewer.models import Site
import siteviewer.main as main
import grapher, multigrapher
from math import sin, cos, atan2, pi

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

def d2r(a):
    return a / 180 * pi

def mi2km(x):
    return 1.60934 * x

def dist(s, lat, lon):
    lats = d2r(s.lat)
    lons = d2r(s.lon)
    latf = d2r(lat)
    lonf = d2r(lon)
    # From http://en.wikipedia.org/wiki/Great-circle_distance
    dlat = abs(lats - latf)
    dlon = abs(lons - lonf)
    n1 = (cos(latf)*sin(dlon))**2
    n2 = (cos(lats)*sin(latf) - (sin(lats)*cos(latf)*cos(dlon)))**2
    d = sin(lats)*sin(latf) + cos(lats)*cos(latf)*cos(dlon)
    return atan2((n1 + n2)** 0.5, d) * 3963.1676


def search(request):
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    query = Site.objects.all().exclude(
                takeoffObj='[[0, 360, "no"]]'
            )
    sites = list(query)
    sites.sort(lambda s1, s2: distCmp(s1, s2, lat, lon))
    for s in sites:
        dmi = dist(s, lat, lon)
        dkm = mi2km(dmi)
        dmi = int(round(dmi))
        dkm = int(round(dkm))
        setattr(s, 'dist_mi', dmi)
        setattr(s, 'dist_km', dkm)
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
