from lxml import etree

class ObservationObj(object):
    def __init__(self, data):
        self.failed = False
        self.readFromData(data)

    def readFromData(self, data):
        tree = etree.fromstring(data)
        mapping = {
            "station_id" : ("name", str),
            "latitude" : ("latitude", float),
            "longitude" : ("longitude", float)
        }
        for tag, (name, conv) in mapping.items():
            v = tree.xpath("/current_observation/%s/text()" % tag)
            if len(v) < 1:
                self.failed = True
                return
            v = v[0]
            if conv:
                v = conv(v)
            setattr(self, name, v)
        self.iid = int(self.name, 36)

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

