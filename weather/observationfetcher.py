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
        sp.check_call(["unzip", outFile, "-d", tmpDir, "-o"])
    else:
        print "Skipping fetch & unzip, station data is current" 

class StationIndex(object):
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

    def getNearestStation(self, lat, lon):
        return self.tree.nearest((lat, lon, lat, lon), 3, 'raw')

def buildIndex():
    si = StationIndex(tmpDir)
    stations = si.getNearestStation(42, 73)
    for s in stations:
        print s

if __name__ == "__main__":
    fetch()
    buildIndex()
