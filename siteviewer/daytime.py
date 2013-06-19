import astral
import datetime

class DayTime(object):

    def __init__(self, site, times):
        self.site = site
        self.times = times
        self.dayIntervals = self.getDayIntervals()

    def getDayIntervals(self):
        site = self.site
        times = self.times
        days = []
        a = astral.Astral()
        dates = set([])
        for dt in times:
           date = datetime.datetime.date(dt)
           dates.add(date)
        dates = list(dates)
        dates.sort()
        for date in dates:
            try:
                sunInfo = a.sun_utc(date, site.lat, site.lon)
            except astral.AstralError:
                continue
            days.append( (sunInfo['sunrise'], sunInfo['sunset']) )
        return days

    def isDay(self, t):
        sunsetFudge = datetime.timedelta(hours=1)
        sunriseFudge = datetime.timedelta(hours=2)
        for sunrise, sunset in self.dayIntervals:
            if t > sunrise + sunriseFudge and t < sunset + sunsetFudge:
                return True
        return False
