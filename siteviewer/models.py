from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    continent = models.CharField(max_length=255)
    lat = models.FloatField()
    lon = models.FloatField()
    altitude = models.FloatField()
    takeoffDirLeft = models.IntegerField()
    takeoffDirRight = models.IntegerField()
    timezone = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def getTakeoffRange(self):
        return (self.takeoffDirLeft, self.takeoffDirRight)
