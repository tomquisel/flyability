## {{{ http://code.activestate.com/recipes/577494/ (r2)
from lxml import etree
import datetime
from weather.models import Forecast, ForecastValue, Scale, TimeSeries

def parseHourlyData(data, site):
    dataMap = { 
        "temp" : TimeSeries("temperature", type="hourly"),
        "dewpt" : TimeSeries("temperature", type="dew point"),
        "pop" : TimeSeries("probability-of-precipitation"),
        "wind" : TimeSeries("wind-speed", type="sustained"),
        "dir" : TimeSeries("direction"),
        "clouds" : TimeSeries("cloud-amount"),
        "humidity" : TimeSeries("humidity")
    }

    tree = etree.fromstring(data)
    times = tree.xpath("//time-layout/start-valid-time/text()")
    scale = Scale().appendTimes(times)
    
    for ts in dataMap.values():
        typeStr = ""
        if ts.type:
            typeStr = "[@type='%s']" % ts.type
        vals = tree.xpath("//%s%s/value/text()" % (ts.name, typeStr))
        ts.appendValues(vals)

    forecast = Forecast(site = site, lat = site.lat, lon = site.lon)
    vals = []
    for name, ts in dataMap.items():
        for i,val in enumerate(ts.values):
            vals.append(ForecastValue(forecast = forecast, 
                                      name = name, value = val,
                                      time = scale.awareTimes[i]))

    return forecast, vals
