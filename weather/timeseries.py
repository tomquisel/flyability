import datetime, pytz

class TimeSeries(object):
    def __init__(self, name, times, values, tz):
        assert(len(values) > 1)
        assert(len(times) == len(values))
        self.name = name
        self.values = values
        self.times = times
        self.tz = pytz.timezone(tz)

    @classmethod
    def fromModels(cls, models, tz):
        assert(len(models) > 1)
        values = [ m.value for m in models ]
        times = [ m.time for m in models ]
        res = cls(models[0].name, times, values, tz)

        # stretch the last data point into the future by one increment
        # In the NOAA weather data, the last data point is actually a time 
        # range. We only store the start. This extends the value to the end.
        res.values.append(res.values[-1])
        diff = res.times[-1] - res.times[-2]
        res.times.append(res.times[-1] + diff)

        return res

    def read(self, tslist, default=None):
        """Returns the value of the series at each timestamp in tslist.
        
        Assumes that tslist is sorted.
        """

        res = []
        awareTsList = self.makeAware(tslist, self.tz)

        before = 0.0
        ind = 0
        after = self.values[ind]
        l = len(self.times)
        for ts in awareTsList:
            while ind < l and ts >= self.times[ind]:
                before = after
                ind += 1
                if ind >= l:
                    before = 0.0
                    after = 0.0
                    break
                after = self.values[ind]
            if ind == 0 or ind >= l:
                v = default
            else :
                bdist = (ts - self.times[ind-1]).total_seconds()
                adist = (ts - self.times[ind]).total_seconds()
                v = (bdist * before + adist * after) / (bdist + adist)
            res.append(v)
        return res

    
    @classmethod
    def makeAware(cls, tslist, tz):
        res = []
        for ts in tslist:
            if ts.tzinfo is None:
                awarets = tz.localize(ts)
            else:
                awarets = ts
            res.append(awarets)
        return res

    hour = datetime.timedelta(hours=1)

    @classmethod
    def range(cls, start, num, inc):
        res = []
        cur = start
        for i in range(0, num):
            res.append(cur)
            cur += inc
        return res

