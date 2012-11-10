#!/usr/bin/env python
import re, json, random, time
from bs4 import BeautifulSoup
from siteviewer.models import Site
from weather.forecast_fetcher import cachingFetch
from geonames import GeonamesClient

geoCli = GeonamesClient('flyability')

def run():
    finishedFile = '/tmp/finished.list'
    base = 'www.paraglidingearth.com'
    toTry = getValidIds(base, '/pgearth/index.php?accueil=monde')
    finished = getFinished(finishedFile)
    toTry = list(set(toTry) - set(finished))
    print "Will scrape %s sites." % len(toTry)
    random.shuffle(toTry)
    try:
        for i in toTry:
            try:
                status = scrape(base,
                                '/pgearth/index.php?site=%s', 
                                '/pgearth/orientation.php?site=%s', 
                                i)
            except:
                time.sleep(random.randint(60, 300))
            else:
                finished.append(i)
                if status != 'hit':
                    time.sleep(random.randint(5, 30))
    finally:
        out = open(finishedFile, 'wb')
        for i in finished:
            print >>out, i
        out.close()

def getValidIds(base, url):
    res = []
    print "Fetching entire list..."
    data = cachingFetch((base, url), (), 365 * 86400)
    print "Parsing list..."
    soup = BeautifulSoup(data)
    for a in soup.find_all("a"):
        m = re.search("index.php\?site=(\d+)", a['href'])
        if m:
            res.append(int(m.group(1)))
    print "Got %s sites." %(len(res))
    return res

def getFinished(f):
    res = [ int(l.strip()) for l in open(f).readlines() ]
    print "Read %s already finished sites" % len(res)
    return res

class MissingDataException(Exception):
    pass

def scrape(base, siteUrl, takeoffUrl, siteId):
    out = Site()

    details1 = {}
    details2 = {}
    try:
        data = cachingFetch((base, siteUrl), siteId, 365 * 86400, details1)
        if data.find("oops, you are trying to") >= 0:
            raise MissingDataException()
        data = preprocess(data)
        soup = BeautifulSoup(data)
        out.id = siteId
        out.name = getName(soup)
        out.continent, out.country, out.state = getGeo(soup)
        out.lat, out.lon, out.altitude = getPos(soup)
        out.timezone = getTZ(out.lat, out.lon)
        out.website = getWebsite(soup)
        out.pgearthSite = "http://" + base + (siteUrl % siteId)

        data = cachingFetch((base, takeoffUrl), siteId, 365 * 86400, details2)
        soup = BeautifulSoup(data)
        out.takeoffObj = getTakeoff(soup)

        print out
        out.save()
    except MissingDataException:
        pass

    if details1.get('hit') and ((len(details2) == 0) or details2.get('hit')):
        return 'hit'
    return 'miss'

def getName(soup):
    tabs = soup.find_all("table")
    return tabs[1].tr.td.span.b.text[3:]

def getGeo(soup):
    div = soup.find("div", "titreMenu")
    res = [ a.text for a in div.find_all("a")]
    return res[1:]

def getPos(soup):
    text = soup.find(text=re.compile("take off : "))
    if text is None:
        raise MissingDataException()
    m = re.search("\((.+?)\)([NS]).+?\((.+?)\)([EW]).+?Elevation\D+?(\d+)", text)
    if m is None:
        raise MissingDataException()
    lat = float(m.group(1))
    ns = m.group(2)
    if ns == "S" : lat = -lat
    lon = float(m.group(3))
    ew = m.group(4)
    if ew == "W" : lon = -lon
    # convert to feet
    alt = float(m.group(5)) * 3.28084
    return lat, lon, alt

def getTZ(lat, lon):
    res = geoCli.find_timezone({'lat': lat, 'lng': lon})
    return res['timezoneId']

def getWebsite(soup):
    txt = soup.find("b", text=re.compile("Website"))
    td = txt.parent.next_sibling.next_sibling
    if td.a:
        return td.a['href']
    return ""

START = 0
END = 1
VAL = 2

def getTakeoff(soup):
    canonicalize = {'perfect':'yes', 'possible':'maybe', 'avoyd': 'no'}
    ranges = [] 
    start = -22.5
    cur = start
    curVal = None
    for tr in soup.find_all("tr"):
        m = re.search("([A-Z]+) :", tr.td.text)
        if not m:
            continue
        d = m.group(1)
        checked = tr.find("input", checked=True)
        if checked:
            val = canonicalize[checked['value']]
        else:
            val = 'no'
        if curVal is not None and val != curVal:
            ranges.append([start, cur, curVal])
            curVal = val
            start = cur
        if curVal is None:
            curVal = val
        cur += 45 
    ranges.append([start, cur, val])
    ranges = adjustTakeoff(ranges)
    return json.dumps(ranges)

def adjustTakeoff(ranges):
    # renormalize the ranges to start at 0
    if ranges[0][VAL] == ranges[-1][VAL]:
        ranges[0][START] = 0
        ranges[-1][END] = 360
    else:
        ranges[0][START] = 0
        ranges.append([360 - 22.5, 360, ranges[0][VAL]])
    return ranges


def preprocess(data):
    # the shitty unescaped JS confuses BeautifulSoup
    data = re.sub(re.compile(r'<.?script.+?/script.?>', re.DOTALL),"",data)
    data = re.sub(re.compile(r'<.?style.+?/style.?>', re.DOTALL),"",data)
    return data

if __name__ == "__main__":
    run()
