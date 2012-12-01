import email.utils
import dateutil.parser

# RFC2822 datetime format
def grabTime(s):
    tup = email.utils.parsedate_tz(s)
    ts = email.utils.mktime_tz(tup)
    return ts

# ISO8601 datetime format
def parseTime(s):
    return dateutil.parser.parse(s)
