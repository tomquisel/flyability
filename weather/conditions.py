
conditionsFilename = "/home/tq/flyability/weather/conditions.txt"

class ConditionMgr(object):
    def __init__(self, filename):
        self.nameToPop = {}
        self.readFile(filename)

    def readFile(self, filename):
        lines = open(filename).readlines()
        for line in lines[1:]:
            fields = line.split(":")
            if len(fields) != 2:
                print "BAD LINE:", line,
                assert(False)
            names,pop = fields
            pop = int(pop.strip())
            names = names.split("|")
            for name in names:
                n = name.strip()
                self.nameToPop[n] = pop

    def getPOP(self, name):
        return self.nameToPop.get(name)

if __name__  == "__main__":
    c = ConditionMgr(conditionsFilename)
    print c.nameToPop

