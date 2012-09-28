import datetime
from django.db import models
from siteviewer.models import Site

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

