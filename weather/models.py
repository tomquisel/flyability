import datetime
from django.db import models
from flyability.siteviewer.models import Site

class Forecast(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetchTime = models.DateTimeField(auto_now_add=True, db_index=True)

class ForecastValue(models.Model):
    forecast = models.ForeignKey(Forecast, db_index=True)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    time = models.DateTimeField()

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

    def appendValue(self, v):
        if v.find(".") >= 0:
            self.values.append(float(v))
        else:
            self.values.append(int(v))


