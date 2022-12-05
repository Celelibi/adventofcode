import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.split()
        a = np.array(data, dtype=np.int32)
        allsums = a.reshape(-1, 1) + a
        idx = np.argwhere(allsums == 2020)
        return np.prod(a[idx[0]])



    def solve2(self, data):
        data = data.split()
        a = np.array(data, dtype=np.int32)
        allsums = a.reshape(-1, 1, 1) + a.reshape(-1, 1) + a
        idx = np.argwhere(allsums == 2020)
        return np.prod(a[idx[0]])



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
