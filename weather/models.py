import datetime, time, json
from django.db import models
from siteviewer.models import Site
from weather.utils import parseTime
from collections import namedtuple

class Forecast(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetch_time = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "Forecast for %f,%f @ %s" % (self.lat, self.lon, self.fetch_time)

ForecastValue = namedtuple('ForecastValue', 'name value time')
ObservationValue = namedtuple('ObservationValue', 'name value')

class ForecastData(models.Model):
    forecast = models.ForeignKey(Forecast)
    data = models.TextField()

    def getData(self, tz):
        vals = self.decode(self.data, tz)
        vals.sort(lambda a,b: self.forecastCmp(a,b))
        return vals

    def setData(self, vals):
        self.data = self.encode(vals)

    @classmethod
    def decode(cls, data, tz):
        vals = json.loads(data)
        converted = []
        for v in vals:
            named = ForecastValue(v[0], v[1], 
                        datetime.datetime.fromtimestamp(v[2], tz))
            converted.append(named)
        return converted

    @classmethod
    def encode(cls, vals):
        converted = []
        for v in vals:
            v2 = [v.name, v.value, int(time.mktime(v.time.timetuple()))]
            converted.append(v2)
        return json.dumps(converted)

    @classmethod
    def forecastCmp(cls, a, b):
        ncmp = cmp(a.name, b.name)
        if ncmp != 0:
            return ncmp
        return cmp(a.time, b.time)


class Observation(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetch_time = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()

class ObservationData(models.Model):
    observation = models.ForeignKey(Observation)
    data = models.TextField()

    def getData(self):
        vals = self.decode(self.data)
        return vals

    def setData(self, vals):
        self.data = self.encode(vals)

    @classmethod
    def decode(cls, data):
        vals = json.loads(data)
        converted = []
        for v in vals:
            named = ObservationValue(v[0], v[1])
            converted.append(named)
        return converted

    @classmethod
    def encode(cls, vals):
        converted = []
        for v in vals:
            v2 = [v.name, v.value]
            converted.append(v2)
        return json.dumps(converted)

class WeatherSummary(models.Model):
    site = models.ForeignKey(Site)
    level = models.CharField(max_length=255)
    data = models.TextField()

    def getData(self):
        converted = []
        data = json.loads(self.data)
        for tup in data:
            o = {}
            o['date'] = datetime.date.fromordinal(int(tup[0]))
            o['score'] = tup[1]
            converted.append(o)
        return converted

    def setData(self, data):
        converted = []
        for o in data:
            ordinal = datetime.date.toordinal(o['date'])
            converted.append((ordinal, o['score']))
        self.data = json.dumps(converted)
