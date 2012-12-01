import datetime, json
from django.db import models
from siteviewer.models import Site
import main

class Forecast(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetch_time = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return "Forecast for %f,%f @ %s" % (self.lat, self.lon, self.fetch_time)

class ForecastValue(models.Model):
    forecast = models.ForeignKey(Forecast)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    time = models.DateTimeField()

    def __unicode__(self):
        return "%s: %s @ %s" % (self.name, self.value, self.time)

def decodeData(data):
    vals = json.loads(data)
    converted = []
    for v in vals:
        v['time'] = main.grabTime(v['time'])
        converted.append(v)
    return converted

def encodeData(vals):
    converted = []
    for v in vals:
        v2 = dict(v)
        v2['time'] = v['time'].isoformat()
        converted.append(v2)
    return json.dumps(converted)
        

class ForecastData(models.Model):
    forecast = models.ForeignKey(Forecast)
    data = models.TextField()

    def getData(self):
        return decodeData(self.data)
    def setData(self, vals):
        self.data = encodeData(vals)


class Observation(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetch_time = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()

class ObservationValue(models.Model):
    observation = models.ForeignKey(Observation)
    name = models.CharField(max_length=100)
    value = models.FloatField()

class ObservationData(models.Model):
    observation = models.ForeignKey(Observation)
    data = models.TextField()

    def getData(self):
        return json.loads(self.data)
    def setData(self, vals):
        self.data = json.dumps(vals)
