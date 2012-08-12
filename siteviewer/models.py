from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    lat = models.FloatField()
    lon = models.FloatField()
    altitude = models.FloatField()
    takeoffDirLeft = models.CharField(max_length=255)
    takeoffDirRight = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def getTakeoffRange(self, numeric=True):
        if numeric:
            dirMap = {
                    'N' : 0,
                    'NE' : 45,
                    'E' : 90,
                    'SE' : 135,
                    'S' : 180,
                    'SW' : 225,
                    'W' : 270,
                    'NW' : 315
                    }
            return (dirMap[self.takeoffDirLeft], dirMap[self.takeoffDirRight])
        else:
            return (self.takeoffDirLeft, self.takeoffDirRight)
