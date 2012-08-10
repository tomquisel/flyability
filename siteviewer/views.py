from siteviewer.models import Site
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import matplotlib.pyplot as plt

import grapher
import predictor
import weather.main as weather

def site(request, name):
    site = get_object_or_404(Site, pk=name)
    return render_to_response('siteviewer/siteview.html', {'site': site})

def forecastImage(request, name):
    site = get_object_or_404(Site, pk=name)
    weatherData = weather.getWeatherData(site)
    flyability = predictor.flyability(site, scale, timeseries)
    #canvas = utils.graphData(scale, timeseries, flyability, canvas = True)
    response = HttpResponse(content_type='image/png')
    #canvas.print_png(response)
    #plt.clf()
    return response
