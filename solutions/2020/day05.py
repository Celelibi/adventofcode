import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.translate(str.maketrans("FBLR", "0101"))
        res = max(int(b, 2) for b in data.splitlines())
        return res



    def solve2(self, data):
        data = data.translate(str.maketrans("FBLR", "0101"))
        seats = np.array(sorted(int(b, 2) for b in data.splitlines()))
        seatidx = np.diff(seats).argmax()
        return seats[seatidx] + 1



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
