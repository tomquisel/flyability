## {{{ http://code.activestate.com/recipes/577494/ (r2)
from lxml import etree
import datetime
from weather.models import ForecastValue

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
    #print "Times len: %s" % (len(times))
    
    values = []
    for internalName,tag in dataMap.items():
        typeStr = ""
        if len(tag) > 1:
            typeStr = "[@type='%s']" % tag[1]
        vals = tree.xpath("//%s%s/value" % (tag[0], typeStr))
        assert(len(vals) == len(times))
        count = 0
        for i,vtag in enumerate(vals):
            txt = vtag.text
            if txt:
                val = ForecastValue(internalName, float(txt), times[i])
                values.append(val)
            count += 1
        #print internalName, " : ", count
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
