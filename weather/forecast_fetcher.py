from weather.caching_fetcher import cachingFetch

hourlyWeather = ['http', 'forecast.weather.gov', '/MapClick.php?lat=%s&lon=%s&FcstType=digitalDWML&w0=t&w1=td&w2=sfcwind&w2u=1&w3=sky&w4=pop&w5=rh']
# http://forecast.weather.gov/MapClick.php?lat=40.96&lon=-72.93&FcstType=digitalDWML&&w0=t&w1=td&w2=sfcwind&w2u=1&w3=sky&w4=pop&w5=rh

fourHourlyWeather = ['https', 'graphical.weather.gov', '/xml/SOAP_server/ndfdXMLclient.php?lat=%s&lon=%s&product=time-series&Unit=e&wgust=wgust&Submit=Submit']
# http://graphical.weather.gov/xml/SOAP_server/ndfdXMLclient.php?lat=40.96&lon=-72.93&&product=time-series&Unit=e&wgust=wgust&Submit=Submit
