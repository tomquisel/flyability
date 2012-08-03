from siteviewer.models import Site
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

import fetcher
import grapher
import utils

def site(request, name):
    site = get_object_or_404(Site, pk=name)
    return render_to_response('siteviewer/siteview.html', {'site': site})

def forecastImage(request, name):
    site = get_object_or_404(Site, pk=name)
    data = fetcher.cachingFetch(fetcher.hourlyWeather, (site.lat, site.lon))
    scale, timeseries = utils.parseData(data)
    canvas = utils.graphData(scale, timeseries, canvas = True)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
