import sys, os, time
import subprocess as sp
from rtree import index
from observation import ObservationObj

url = "w1.weather.gov/xml/current_obs/all_xml.zip"
tmpDir = '/var/django/observationtmp'

def fetch():
    outFile = "%s/all_xml.zip" % tmpDir
    if os.path.getmtime(outFile) < time.time() - 30 * 60:
        sp.check_call(["curl", url, "-o", outFile])
        sp.check_call(["unzip", "-o", outFile, "-d", tmpDir])
    else:
        print "Skipping fetch & unzip, station data is current" 

class ObservationIndex(object):
    def __init__(self, stationDir):
        self.stationDir = stationDir
        self.tree = index.Index()
        self.generate()

    def generate(self):
        for fn in os.listdir(self.stationDir):
            ext = fn.split(".")[-1]
            if ext != 'xml':
                continue
            fn = os.path.join(self.stationDir, fn)
            obs = ObservationObj(open(fn).read())
            if obs.failed:
                continue
            lat = obs.latitude
            lon = obs.longitude
            self.tree.insert(obs.iid, (lat, lon, lat, lon), obj=obs)

    def getNearest(self, lat, lon):
        return self.tree.nearest((lat, lon, lat, lon), 1, 'raw')

def buildIndex():
    si = ObservationIndex(tmpDir)
    return si

if __name__ == "__main__":
    fetch()
    index = buildIndex()
    lat = float(sys.argv[1])
    lon = float(sys.argv[2])
    stations = index.getNearest(lat, lon)
    for s in stations:
        print "DIST:", ((lat - s.latitude)**2 + (lon - s.longitude)**2) ** 0.5
        print s
