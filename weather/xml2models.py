## {{{ http://code.activestate.com/recipes/577494/ (r2)
from lxml import etree
import datetime
from weather.models import Forecast, ForecastValue

def parseHourlyData(data):
    dataMap = { 
        "temp" : ("temperature", "hourly"),
        "dewpt" : ("temperature", "dew point"),
        "pop" : ("probability-of-precipitation",),
        "wind" : ("wind-speed", "sustained"),
        "dir" : ("direction",),
        "clouds" : ("cloud-amount",),
        "humidity" : ("humidity",)
    }
    return parseData(data, dataMap)

def parseFourHourlyData(data):
    dataMap = { 
        "gust" : ("wind-speed", "gust")
    }
    return parseData(data, dataMap)

def parseData(data, dataMap):

    tree = etree.fromstring(data)
    times = tree.xpath("//time-layout/start-valid-time/text()")
    times = readTimes(times)
    
    values = []
    for internalName,tag in dataMap.items():
        typeStr = ""
        if len(tag) > 1:
            typeStr = "[@type='%s']" % tag[1]
        vals = tree.xpath("//%s%s/value/text()" % (tag[0], typeStr))
        for i,v in enumerate(vals):
            values.append(ForecastValue(name = internalName, value = float(v),
                                        time = times[i]))
    return values

def readTimes(times):
    class TZ (datetime.tzinfo):
        def __init__(self, offset):
            self.offset = datetime.timedelta(hours=offset)
        def utcoffset(self, d):
            return self.offset
        def dst(self, d):
            return datetime.timedelta(hours=0)
    
    res = []

    for s in times:
        timeStr = s[:-6]
        tzStr = s[-6:]

        tz = TZ(int(tzStr.split(":")[0]))
        t = datetime.datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
        at = t.replace(tzinfo=tz)
        res.append(at)
    return res
