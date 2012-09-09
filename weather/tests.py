from django.test import TestCase
from timeseries import TimeSeries
import datetime, pytz

class TimeSeriesTest(TestCase):
    def test_interpolate(self):
        """ test TimeSeries.interpolate """
        tzstr = "US/Eastern"
        tz = pytz.timezone(tzstr)
        h = TimeSeries.hour
        n = datetime.datetime.now()
        times1 = [n, n+h, n+2*h, n+3*h]
        times2 = [n, n+3*h]
        times2 = TimeSeries.makeAware(times2, tz)

        values = [6.0, 8.0]
        ts = TimeSeries("test", times2, values, tzstr)
        res = ts.interpolate(times1)
        target = [6.0, 6.66667, 7.33333, 8.0]
        for i in range(len(res)):
            self.failUnlessAlmostEqual(res[i], target[i], places=4)

        times3 = [n-h, n+2*h, n+4*h]
        res = ts.interpolate(times3)
        target = [None, 7.3333333, None]
        for i in range(len(res)):
            self.failUnlessAlmostEqual(res[i], target[i], places=4)
