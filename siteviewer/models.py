from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    state = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    continent = models.CharField(max_length=255, default='')
    lat = models.FloatField()
    lon = models.FloatField()
    altitude = models.FloatField()
    takeoffDirLeft = models.IntegerField()
    takeoffDirRight = models.IntegerField()
    timezone = models.CharField(max_length=255)
    website = models.CharField(max_length=255, default='')
    pgearthSite = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return self.name

    def getTakeoffRange(self):
        return (self.takeoffDirLeft, self.takeoffDirRight)
