import datetime, pytz
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
import matplotlib.pyplot as plt

from siteviewer.models import Site
from weather.timeseries import TimeSeries
import weather.main as weather
import grapher
import predictor

def site(request, name):
    site = get_object_or_404(Site, pk=name)
    return render_to_response('siteviewer/siteview.html', {'site': site})

def forecastImage(request, name):
    site = get_object_or_404(Site, pk=name)
    seriesDict = weather.getWeatherData(site)
    tz = pytz.timezone(site.timezone)
    times = TimeSeries.range(datetime.datetime.now(), 168, TimeSeries.hour)
    awareTimes = TimeSeries.makeAware(times, tz)
    flyability = predictor.flyability(site, awareTimes, seriesDict)
    seriesDict['flyability'] = flyability
    canvas = grapher.plot(times, seriesDict, canvas = True)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    plt.clf()
    return response
