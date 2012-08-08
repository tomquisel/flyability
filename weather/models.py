from django.db import models
from flyability.siteviewer.models import Site

class Forecast(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetchTime = models.DateTimeField(auto_now_add=True)

class ForecastValue(models.Model):
    forecast = models.ForeignKey(Forecast)
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
