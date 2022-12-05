from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.split(",")
        lastseen = {int(v): i for i, v in enumerate(data[:-1])}
        lastvalue = int(data[-1])

        for i in range(len(lastseen), 2020 - 1):
            if lastvalue not in lastseen:
                newvalue = 0
            else:
                newvalue = i - lastseen[lastvalue]

            lastseen[lastvalue] = i
            lastvalue = newvalue

        return lastvalue



    def solve2(self, data):
        data = data.split(",")
        lastseen = {int(v): i for i, v in enumerate(data[:-1])}
        lastvalue = int(data[-1])

        for i in range(len(lastseen), 30000000 - 1):
            if lastvalue not in lastseen:
                newvalue = 0
            else:
                newvalue = i - lastseen[lastvalue]

            lastseen[lastvalue] = i
            lastvalue = newvalue

        return lastvalue



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
