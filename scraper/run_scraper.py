#!/usr/bin/env python
import re, json, random, time
from bs4 import BeautifulSoup
from siteviewer.models import Site
from weather.forecast_fetcher import cachingFetch
from geonames import GeonamesClient

geoCli = GeonamesClient('flyability')

def run():
    base = 'www.paraglidingearth.com'
    # only fetch United States sites
    site_id_fetcher = SiteIdFetcher(base, 223, 224)
    for site in site_id_fetcher.get_all_site_ids():
        #try:
        status = scrape(base,
                        '/pgearth/index.php?site=%s', 
                        '/pgearth/orientation.php?site=%s', 
                        site)
        #except Exception, e:
        #    time.sleep(random.randint(60, 300))
        #else:
        if status != 'hit':
            time.sleep(random.randint(5, 30))

class SiteIdFetcher(object):
    def __init__(self, url_base, start, end):
        self.state_file  = '/tmp/site_id_fetcher_state.json'
        self.path_prefix = '/pgearth/fiche_pays_imprimable.php?pays='
        self.url_base = url_base
        self.max_country = end
        try:
            self.load_state()
        except IOError, e:
            self.state = {
                'next_country_id': start,
                'next_site_id_index': 0,
                'site_ids': [],
            }
            self.save_state()

    def load_state(self):
        self.state = json.load(open(self.state_file))

    def save_state(self):
        json.dump(self.state, open(self.state_file, 'wb'), indent=1)

    def get_all_site_ids(self):
        while True:
            # record that the client successfully processed the last site_id
            self.save_state()
            #print self.state
            while self.needs_more_site_ids():
                if self.done():
                    return
                self.load_next_site_id_chunk()
            yield self.state['site_ids'][self.state['next_site_id_index']]
            self.state['next_site_id_index'] += 1
    
    def load_next_site_id_chunk(self):
        path = "%s%s" % (self.path_prefix, self.state['next_country_id'])
        print "Fetching site ids for country %s..." % \
                self.state['next_country_id']
        ids = self.fetch_site_ids_for_country(self.url_base, path)
        self.state['site_ids'].extend(ids)
        self.state['next_country_id'] += 1
        self.save_state()
        return ids
    
    @staticmethod
    def fetch_site_ids_for_country(base, path): 
        ids = []
        data = cachingFetch((base, path), (), 365 * 86400)
        print "Parsing %s" % path
        soup = BeautifulSoup(data)
        for img in soup.find_all("img"):
            m = re.search("windrose.php?.*id_site=(\d+)", img['src'])
            if m:
                ids.append(int(m.group(1)))
        print "Got %s site ids." %(len(ids))
        return ids

    def done(self):
        return self.state['next_country_id'] >= self.max_country

    def needs_more_site_ids(self): 
        return len(self.state['site_ids']) <= self.state['next_site_id_index']


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
