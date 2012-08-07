## {{{ http://code.activestate.com/recipes/577494/ (r2)
from xml.parsers.expat import ParserCreate
import weather.models as wmods

class Scale:
    def __init__(self, valuetag="start-valid-time"):
        self.valuetag = valuetag
        self.times = []
        self.awareTimes = []

    def appendTime(self, s):
        class TZ (datetime.tzinfo):
            def __init__(self, offset):
                self.offset = datetime.timedelta(hours=offset)
            def utcoffset(self, d):
                return self.offset
            def dst(self, d):
                return datetime.timedelta(hours=0)

        timeStr = s[:-6]
        tzStr = s[-6:]

        tz = TZ(int(tzStr.split(":")[0]))
        t = datetime.datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%S")
        at = t.replace(tzinfo=tz)
        self.times.append(t)
        self.awareTimes.append(at)

class TimeSeries:
    def __init__(self, tag, valuetag="value", type=None):
        self.tag = tag
        self.valuetag = valuetag
        self.type = type
        self.units = None
        self.values = []

    def appendVal(self, v):
        if v.find(".") >= 0:
            self.values.append(float(v))
        else:
            self.values.append(int(v))

##############################################################################

def summarize(json, level=0):
    t = type(json)
    items = []
    if t == dict:
        keys = json.keys()[:10]
        print "%slen=%s" % (" " * level, len(json))
        for key in keys:
            print "%s%s:" % (" " * level, key)
            summarize(json[key], level+1)
    elif t == list:
        print "%slen=%s" % (" " * level, len(json))
        for i in range(0,min(10,len(json))):
            summarize(json[i], level+1)
    else:
        print (" " * level) + json

def printts(scale, timeseries):
    l = 10
    for t in scale.times[:l]:
        print t
    for ts in timeseries:
        print ts.tag, ts.type, ts.units
        for v in ts.values[:l]:
            print v

##############################################################################

class Xml2TimeSeries:
    LIST_TAGS = ['COMMANDS']
    
    def __init__(self, scale, tsList, data=None):
        self.scale = scale
        self.tsList = tsList
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.currentTS = None
        if data:
            self.feed(data)
            self.close()
        
    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def checkSeriesStart(self, tag, attrs):
        for ts in self.tsList:
            if ts.tag != tag:
                continue
            if ts.type is not None:
                if ts.type != attrs.get('type'):
                    continue
            # we found a time series matching this section
            assert self.currentTS is None
            self.currentTS = ts
            units = attrs.get('units')
            ts.units = units

    def start(self, tag, attrs):
        assert self._data.strip() == ''
        self.checkSeriesStart(tag, attrs)
        #print "START", repr(tag)
        self._data = ''

    def end(self, tag):
        #print "END", repr(tag)

        data = self._data
        if self.currentTS and tag == self.currentTS.valuetag:
            self.currentTS.appendVal(data)
        if self.currentTS and tag == self.currentTS.tag:
            self.currentTS = None
        if tag == self.scale.valuetag:
            self.scale.appendTime(data)

        self._data = ''

    def data(self, data):
        self._data = data

##############################################################################

class Xml2Json:
    LIST_TAGS = ['COMMANDS']
    
    def __init__(self, data = None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()
        
    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        assert self._data.strip() == ''
        #print "START", repr(tag)
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        #print "END", repr(tag)
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1: #leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else: #force into a list
                data = [{k:v} for k, v in last_tag[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag:data}
        self._data = ''

    def data(self, data):
        self._data = data


# >>> Xml2Json('<doc><tag><subtag>data</subtag><t>data1</t><t>data2</t></tag></doc>').result
# {u'doc': {u'tag': {u'subtag': u'data', u't': [u'data1', u'data2']}}}
## end of http://code.activestate.com/recipes/577494/ }}}

