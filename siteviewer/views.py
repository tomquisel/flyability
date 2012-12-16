import datetime, time
import json
from django.http import HttpResponse, Http404 
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.views.decorators.cache import cache_control
from siteviewer.models import Site
import siteviewer.main as main
import grapher, multigrapher
from math import sin, cos, atan2, pi
import weather.main as weather
import siteviewer.mapstate as mapstate
from profiler import profile

def index(request):
    sites = main.getAllSites();

    sitesobj = []
    for i,s in enumerate(sites):
        out = {}
        out['lat'] = s.lat
        out['lon'] = s.lon
        out['name'] = s.name
        out['pos'] = i
        out['id'] = s.id
        sitesobj.append(out)

    env = { 'sitesobj' : json.dumps(sitesobj) }
    return render_to_response('siteviewer/index.html', env,
                              context_instance=RequestContext(request))
def sitelist(request):
    sites = main.getAllSites();

    def siteCmp(a,b):
        scmp = cmp(a.state, b.state)
        if scmp != 0:
            return scmp
        return cmp(a.name,b.name)
    sites.sort(siteCmp)

    states = []
    sitesobj = []
    lastState = None
    for s in sites:
        if lastState != s.state:
            sitesobj.append({'state' : s.state})
            states.append(s.state)
            lastState = s.state
        out = {}
        out['name'] = s.name
        out['state'] = s.state
        out['country'] = s.country
        sitesobj.append(out)

    env = { 'sites' : sitesobj , 'states' : states }
    return render_to_response('siteviewer/sitelist.html', env,
                              context_instance=RequestContext(request))

def site(request, country, state, name):
    sites = Site.objects.filter(name=name).\
            filter(state=state).\
            filter(country=country)
    if len(sites) == 0:
        raise Http404
    assert(len(sites) == 1)
    site = sites[0]
    env = {'site' : site}
    try:
        mgr = main.ForecastMgr(site)
        days = mgr.getDays()
        env['days'] = days
    except weather.NoWeatherDataException: 
        pass
    return render_to_response('siteviewer/siteview.html', env,
                              context_instance=RequestContext(request))

def summary(request):
    id = int(main.getOr404(request.GET, 'id'))
    site = get_object_or_404(Site, pk=id)
    main.addSiteDetails(site)
    env = {'site' : site}
    return render_to_response('siteviewer/sitesummary.html', env,
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


#@profile("search.prof")
def search(request):
    lat = float(main.getOr404(request.GET, 'lat'))
    lon = float(main.getOr404(request.GET, 'lon'))
    query = main.getOr404(request.GET, 'query')
    request.session['query'] = query
    t1 = time.time()
    sites = main.getAllSites()
    t2 = time.time()
    sites.sort(lambda s1, s2: distCmp(s1, s2, lat, lon))
    t3 = time.time()
    res = sites[:10]
    for s in res:
        dmi = dist(s, lat, lon)
        dkm = mi2km(dmi)
        dmi = int(round(dmi))
        dkm = int(round(dkm))
        setattr(s, 'dist_mi', dmi)
        setattr(s, 'dist_km', dkm)
        main.addSiteDetails(s)
    t4 = time.time()

    print "Times: %s %s %s" % (t2-t1, t3-t2, t4-t3)

    env = { 'sites' : res }
    return render_to_response('siteviewer/search_body.inc', env,
                              context_instance=RequestContext(request))

@cache_control(public=True, max_age=3600*24*365)
def windDir(request, wind, siteid, size):
    wind, siteid, size = int(wind), int(siteid), int(size)
    site = get_object_or_404(Site, pk=siteid)
    showWind = wind >= 0
    response = multigrapher.runGrapher(
            lambda : grapher.drawWindDir(wind, site.getTakeoffObj(), size, 
                                         showWind)
    )
    if isinstance(response, Exception):
        raise response
    return response

# unused
#def windArrow(request, wind, left, right, size):
#    wind, left, right, size = int(wind), int(left), int(right), int(size)
#    response = multigrapher.runGrapher(
#            lambda : grapher.drawArrow(wind, left, right, size)
#    )
#    return response
#
#def state(request, country, state):
#    sites = Site.objects.filter(
#                             country = country
#                         ).filter(
#                             state = state
#                         )
#    env = {'sites' : sites, 'country' : country, 'state' : state}
#    return render_to_response('siteviewer/statelist.html', env,
#                              context_instance=RequestContext(request))
#def country(request, country):
#    sites = Site.objects.filter(country = country)
#    env = {'sites' : sites, 'country' : country}
#    return render_to_response('siteviewer/countrylist.html', env,
#                              context_instance=RequestContext(request))
#
#def allSiteNames(request):
#    sites = Site.objects.all()
#    names = [ "%s, %s, %s" % (s.name, s.state, s.country) for s in sites]
#    env = { 'names' : names }
#    return render_to_response('siteviewer/api/allsitenames.html', env,
#                              context_instance=RequestContext(request))
#
