from django.db import models
import json

class Site(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=255, default='')
    continent = models.CharField(max_length=255, default='')
    lat = models.FloatField()
    lon = models.FloatField()
    altitude = models.FloatField()
    takeoffObj = models.TextField()
    timezone = models.CharField(max_length=255)
    website = models.CharField(max_length=255, default='')
    pgearthSite = models.CharField(max_length=255, default='')

    def __unicode__(self):
        name = ", ".join((self.name, self.state, self.country, self.continent))
        pos = "%s, %s @ %s ft, %s" % (self.lat, self.lon, self.altitude, 
                                      self.timezone)
        takeoff = "takeoff: %s" % self.takeoffObj
        res = "++++++++++\n"
        res += "\n".join((name, pos, takeoff, self.website, self.pgearthSite))
        res += "\n----------"
        return res

    def getTakeoffObj(self):
        if getattr(self, 'takeoffCache', None):
            return self.takeoffCache

        self.takeoffCache = {}
        if self.takeoffObj:
            self.takeoffCache = json.loads(self.takeoffObj)
        return self.takeoffCache
