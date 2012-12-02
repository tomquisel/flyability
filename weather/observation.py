from lxml import etree
from weather.models import Observation, ObservationValue
import datetime, pytz
from weather.utils import grabTime

class ObservationObj(object):
    def __init__(self, data):
        self.failed = False
        self.mapping = {
            "station_id" : ("name", str, None, None),
            "latitude" : ("latitude", float, -90.0, 90.0),
            "longitude" : ("longitude", float, -180.0, 180.0),
            "temp_f" : ("temp", float, -200.0, 200.0),
            "dewpoint_f" : ("dewpt", float, -200.0, 200.0),
            "wind_degrees" : ("dir", float, 0.0, 360.0),
            "wind_mph" : ("wind", float, 0.0, 300.0),
            "weather" : ("weather", str, None, None),
            "observation_time_rfc822" : ("time", grabTime, None, None)
        }
        self.readFromData(data)

    def readFromData(self, data):
        tree = etree.fromstring(data)
        for tag, (name, conv, minv, maxv) in self.mapping.items():
            v = tree.xpath("/current_observation/%s/text()" % tag)
            if len(v) < 1:
                self.failed = True
                return
            v = v[0]
            if conv:
                v = conv(v)
            if minv is not None and v < minv:
                self.failed = True
                return
            if maxv is not None and v > maxv:
                self.failed = True
                return
            setattr(self, name, v)
        self.iid = int(self.name, 36)

    def toDjangoModels(self, site, conditionMgr):
        dt = datetime.datetime.fromtimestamp(self.time)
        tz = pytz.timezone(site.timezone)
        locdt = tz.localize(dt)
        obs = Observation(site=site, lat=self.latitude, lon=self.longitude,
                          time=locdt)
        skip = set(["name", "weather", "time", "latitude", "longitude"])
        values = []
        for v in self.mapping.values():
            name = v[0]
            if name in skip:
                continue
            o = ObservationValue( name, getattr(self, name) )
            values.append(o)
        pop = conditionMgr.getPOP(self.weather)
        if pop is None:
            print "WARNING: unknown weather type '%s'" % self.weather
            pop = 0
        o = ObservationValue( "pop", pop )
        values.append(o)
        return (obs, values)

    def __unicode__(self):
        s = "Observation:\n"
        names = dir(self)
        for n,v in self.__dict__.items():
            if callable(v):
                continue
            s += "%s : %s\n" % (n, v)
        return s

    def __str__(self):
            return unicode(self).encode('utf-8')
