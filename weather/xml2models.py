## {{{ http://code.activestate.com/recipes/577494/ (r2)
from lxml import etree
import datetime
from weather.models import Forecast, ForecastValue


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
        vals = tree.xpath("//%s%s/value/text()" % (ts.tag, typeStr))
        ts.appendValues(vals)

    forecast = Forecast(site = site, lat = site.lat, lon = site.lon)
    vals = []
    for name, ts in dataMap.items():
        for i,val in enumerate(ts.values):
            vals.append(ForecastValue(forecast = forecast, 
                                      name = name, value = val,
                                      time = scale.awareTimes[i]))

    return forecast, vals

##############################################################################

class Scale(object):
    def __init__(self):
        self.times = []
        self.awareTimes = []

    def appendTimes(self, times):
        for time in times:
            self.appendTime(time)
        return self

    def appendTime(self, s):
        class TZ (datetime.tzinfo):
            def __init__(self, offset):
                self.offset = datetime.timedelta(hours=offset)
            def utcoffset(self, d):
                return self.offset
            def dst(self, d):
                return datetime.timedelta(hours=0)

        timeStr = s[:-6]
        tzStr = s[-6:]

        tz = TZ(int(tzStr.split(":")[0]))
        t = datetime.datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
        at = t.replace(tzinfo=tz)
        self.times.append(t)
        self.awareTimes.append(at)

class TimeSeries(object):
    def __init__(self, tag, valuetag="value", type=None):
        self.tag = tag
        self.valuetag = valuetag
        self.type = type
        self.units = None
        self.values = []

    def appendValues(self, vs):
        for v in vs:
            self.appendValue(v)

    def appendValue(self, v):
        if v.find(".") >= 0:
            self.values.append(float(v))
        else:
            self.values.append(int(v))

##############################################################################
