
class Sum(object):
    def __init__(self, timeunit = 1000*60):
        self.__sum = 0
        self.__count = 0
        self.__clock = None
        self.__timeunit = timeunit
    
    def add(self, clock, v):
        if not self.__clock:
            self.__clock = clock
        else:
            if int(self.__clock / self.__timeunit) != int(clock / self.__timeunit):
                return False
            self.__clock = clock
        self.__sum += v
        self.__count += 1

        return True

    def write(self, f):
        if not self.__count:
            return
        v = float(self.__sum / self.__count)
        f.writelines(('{},{}\n'.format(self.__clock,v)))

ff = open('cpmyard.min.csv','w')

f = open('cpmyard.csv')

header = None
s = Sum()
for l in f.readlines():
    if not header:
        header = l
        ff.writelines((header,))
    elif l:
        (clock, v) =l.split(',')
        clock = int(clock)
        v = float(v)
        if not s.add(clock ,v):
            s.write(ff)
            s = Sum()
            s.add(clock, v)
s.write(ff)
ff.close()
f.close()