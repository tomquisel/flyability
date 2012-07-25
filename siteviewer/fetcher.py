import sys,os
import httplib

hourlyWeather = ['forecast.weather.gov', '/MapClick.php?lat=42.66580&lon=-73.79900&FcstType=digitalDWML']
#query = ['graphical.weather.gov', '/xml/SOAP_server/ndfdXMLclient.php?whichClient=NDFDgen&lat=42.044258&lon=-73.492621&product=time-series&Unit=e&temp=temp&wspd=wspd&wdir=wdir&sky=sky&wx=wx&precipa_r=precipa_r&wgust=wgust&Submit=Submit']

def fetch(query):
    conn = httplib.HTTPConnection(query[0])
    conn.request("GET", query[1])
    r = conn.getresponse()
    print r.status, r.reason
    if r.status != httplib.OK:
        return None
    data = r.read()
    conn.close()
    return data

def cachingFetch(query):
    cache = "result.xml"
    if os.path.exists(cache):
        print "cache hit"
        data = open(cache).read()
        return data
    print "cache miss"
    data = fetch(query)
    if data is None:
        return None
    open(cache, "wb").write(data)
    return data
