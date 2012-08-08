import sys, os, time
import httplib
import hashlib

hourlyWeather = ['forecast.weather.gov', '/MapClick.php?lat=%s&lon=%s&FcstType=digitalDWML']
fourHourlyWeather = ['graphical.weather.gov', '/xml/SOAP_server/ndfdXMLclient.php?lat=%s&lon=%s&product=time-series&Unit=e&wgust=wgust&Submit=Submit']

def fetch(query, params):
    conn = httplib.HTTPConnection(query[0])
    conn.request("GET", query[1] % params)
    r = conn.getresponse()
    print r.status, r.reason
    if r.status != httplib.OK:
        return None
    data = r.read()
    conn.close()
    return data


def cachingFetch(query, params):
    cacheDir = '/var/django/cache/'
    key = hashit( (query, params) )
    fn = cacheDir + key
    print fn,
    if os.path.exists(fn):
        if os.path.getmtime(fn) > (time.time() - 600):
            data = open(fn).read()
            print " cache hit"
            return data
    print " cache miss"
    data = fetch(query, params)
    if data is None:
        return None
    open(fn, "wb").write(data)
    return data

def hashit(arg):
    sha1 = hashlib.sha1() 
    sha1.update(str(arg))
    return sha1.hexdigest()[:16]
