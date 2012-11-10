#!/usr/bin/env python
import re
from bs4 import BeautifulSoup
from siteviewer.models import Site
from weather.forecast_fetcher import cachingFetch
from geonames import GeonamesClient

geo_cli = GeonamesClient('flyability')

def getName(soup):
    tabs = soup.find_all("table")
    return tabs[1].tr.td.span.b.text[3:]

def getGeo(soup):
    div = soup.find("div", "titreMenu")
    res = [ a.text for a in div.find_all("a")]
    return res[1:]

def getPos(soup):
    text = soup.find(text=re.compile("take off : "))
    m = re.search("\((.+?)\)([NS]).+\((.+?)\)([EW]).+Elevation\D+(\d+)", text)
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
    res = geo_cli.find_timezone({'lat': lat, 'lng': lon})
    return res['timezoneId']

def getWebsite(soup):
    txt = soup.find("b", text=re.compile("Website"))
    td = txt.parent.next_sibling.next_sibling
    return td.a.text

def scrape(url, query):
    out = Site()

    data = cachingFetch(url, query, 86400)
    soup = BeautifulSoup(data)
    out.name = getName(soup)
    out.continent, out.country, out.state = getGeo(soup)
    out.lat, out.lon, out.altitude = getPos(soup)
    out.timezone = getTZ(out.lat, out.lon)
    out.website = getWebsite(soup)
    out.pgearthSite = "http://" + url[0] + (url[1] % query)

    print out


def run():
    scrape(['www.paraglidingearth.com', '/pgearth/index.php?site=%s'], 7299)

if __name__ == "__main__":
    run()
