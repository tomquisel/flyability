#!/usr/bin/env python
import sys, os
import fetcher
import grapher
import utils


data = fetcher.cachingFetch(fetcher.hourlyWeather)

scale, timeseries = utils.parseData(data)
utils.graphData(scale, timeseries)

