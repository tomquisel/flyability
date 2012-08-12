import datetime
from django.db import models
from flyability.siteviewer.models import Site

class Forecast(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetchTime = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "Forecast for %f,%f @ %s" % (self.lat, self.lon, self.fetchTime)

class ForecastValue(models.Model):
    forecast = models.ForeignKey(Forecast)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    time = models.DateTimeField()

    def __unicode__(self):
        return "%s: %s @ %s" % (self.name, self.value, self.time)

class Observation(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetchTime = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()

class ObservationValue(models.Model):
    observation = models.ForeignKey(Observation)
    name = models.CharField(max_length=100)
    value = models.FloatField()

################################################################
# these aren't django models, but they're useful data types

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
    def __init__(self, name, type=None):
        self.type=type
        self.name = name
        self.values = []

    def appendValues(self, vs):
        for v in vs:
            self.appendValue(v)
        return self

    def appendValue(self, v):
        if type(v) is str:
            if v.find(".") >= 0:
                v = float(v)
            else:
                v = int(v)
        self.values.append(v)
        return self


