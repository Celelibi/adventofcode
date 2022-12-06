from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        return next(i + 4 for i in range(len(data)) if len(set(data[i:i+4])) == 4)



    def solve2(self, data):
        return next(i + 14 for i in range(len(data)) if len(set(data[i:i+14])) == 14)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
