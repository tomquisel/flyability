from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    altitude = models.FloatField()
    takeoffDirLeft = models.CharField(max_length=20)
    takeoffDirRight = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name
