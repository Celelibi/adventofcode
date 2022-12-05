import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = np.array([list(l) for l in data.splitlines()])
        data = (data == "#")
        y = np.arange(data.shape[0])
        x = y * 3 % data.shape[1]
        return data[y, x].sum()



    def solve2(self, data):
        data = np.array([list(l) for l in data.splitlines()])
        data = (data == "#")

        slopes = np.array([1, 3, 5, 7])
        y = np.arange(data.shape[0]).reshape(-1, 1)
        x = y * slopes % data.shape[1]
        res1 = data[y, x].sum(axis=0).prod()
        y = np.arange(data.shape[0], step=2)
        x = y // 2 % data.shape[1]
        return res1 * data[y, x].sum()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
