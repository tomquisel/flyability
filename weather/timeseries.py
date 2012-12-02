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

    def add(self, time, value):
        ind = 0
        for i,t in enumerate(self.times):
            if time < t:
                ind = i
                break
        self.times.insert(ind, time)
        self.values.insert(ind, value)

    def interpolate(self, tslist, default=None):
        """Returns the value of the series at each timestamp in tslist.
        
        Assumes that tslist is sorted.
        """

        res = []
        awareTsList = self.makeAware(tslist, self.tz)

        before = None
        ind = 0
        after = self.values[ind]
        l = len(self.times)
        for ts in awareTsList:
            # this is necessary if ts == self.times[-1]
            if ind < l and ts == self.times[ind]:
                res.append(after)
                continue
            # advance our position in self.values
            while ind < l and ts > self.times[ind]:
                before = after
                ind += 1
                if ind >= l:
                    after = None
                else:
                    after = self.values[ind]
            # if we're before the start of self.times or after the end 
            # of self.times, just use the default value
            if before is None or after is None:
                v = default
            else:
                # compute our value as the weighted average of before and after
                bdist = abs((ts - self.times[ind-1]).total_seconds())
                adist = abs((ts - self.times[ind]).total_seconds())
                aweight = 1 - adist / (adist + bdist)
                bweight = 1 - aweight
                v = bweight * before + aweight * after
            res.append(v)
        assert(len(res) == len(tslist))
        return res

    def readNatural(self):
        return (self.times, self.values)
    
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
        """Generates a sequence of times"""
        res = []
        cur = start
        for i in range(0, num):
            res.append(cur)
            cur += inc
        return res

    @classmethod
    def stripTrailingNones(cls, values):
        newvalues = []
        skip = True
        for i in range(len(values)-1, -1, -1):
            if values[i] != None:
                skip = False
            if not skip:
                newvalues.append(values[i])
        newvalues.reverse()
        return newvalues

    @classmethod
    def substitute(cls, values, frm, to):
        def sub(v):
            if v == frm:
                return to
            return v
        return map(sub, values)

