from django.db import models
from siteviewer.models import Site

# structure:
# 
# forecast table: id, site, lat, lon, when_fetched
# forecast_value tale: id, forecast_id, name, time, value
# observation: id, name, time, value

class Forecast(models.Model):
    site = models.ForeignKey(Site)
    lat = models.FloatField()
    lon = models.FloatField()
    fetchTime = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField()

class ForecastValue(models.Model):
    forecast = models.ForeignKey(Forecast)
    name = models.CharField(max_length=100)
    value = models.FloatField()

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
