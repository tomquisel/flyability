#!/usr/bin/env python
import sys, os
import fetcher
import grapher
import utils


loc = (42.0443, -73.492626)
data = fetcher.cachingFetch(fetcher.hourlyWeather, loc)

scale, timeseries = utils.parseData(data)
utils.graphData(scale, timeseries)

