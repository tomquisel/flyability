import sys, os, time
import httplib
import hashlib

hourlyWeather = ['forecast.weather.gov', '/MapClick.php?lat=%s&lon=%s&FcstType=digitalDWML&w0=t&w1=td&w2=sfcwind&w2u=1&w3=sky&w4=pop&w5=rh']
# http://forecast.weather.gov/MapClick.php?lat=40.96&lon=-72.93&FcstType=digitalDWML&&w0=t&w1=td&w2=sfcwind&w2u=1&w3=sky&w4=pop&w5=rh

fourHourlyWeather = ['graphical.weather.gov', '/xml/SOAP_server/ndfdXMLclient.php?lat=%s&lon=%s&product=time-series&Unit=e&wgust=wgust&Submit=Submit']
# http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?lat=40.96&lon=-72.93&&product=time-series&Unit=e&wgust=wgust&Submit=Submit

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4"

def fetch(url, params):
    print "Fetching %s%s" % (url[0],url[1] % params)
    conn = httplib.HTTPConnection(url[0])
    conn.request("GET", url[1] % params, headers={'user-agent' : agent})
    r = conn.getresponse()
    print r.status, r.reason
    if r.status != httplib.OK:
        return None
    data = r.read()
    conn.close()
    return data


def cachingFetch(url, params, expiration=600, details={}):
    cacheDir = '/var/django/cache/'
    key = hashit( (url, params) )
    fn = cacheDir + key
    print fn,
    if os.path.exists(fn):
        if os.path.getmtime(fn) > (time.time() - expiration):
            data = open(fn).read()
            print " cache hit"
            details['hit'] = True
            details['success'] = True
            return data
    print " cache miss"
    data = fetch(url, params)
    if data is None:
        details['success'] = False
        return None
    open(fn, "wb").write(data)
    details['hit'] = False
    details['success'] = True
    return data

def hashit(arg):
    sha1 = hashlib.sha1() 
    sha1.update(str(arg))
    return sha1.hexdigest()[:16]
