import numpy as np

from libadventofcode import base
from libadventofcode import registry



def tribo(n):
    glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
    return np.linalg.matrix_power(glider, n).dot([0, 1, 1])[0]



class Solver(base.Solver):
    def solve1(self, data):
        data = np.array((data + "0").splitlines(), dtype=np.int)
        data.sort()
        diff = np.diff(data)
        res = (diff == 1).sum() * ((diff == 3).sum() + 1)
        return res



    def solve2(self, data):
        data = np.array((data + "0").splitlines(), dtype=np.int)
        data.sort()
        diff = np.insert(np.diff(np.append(data, data[-1] + 3)), 0, 0)
        diff = np.diff((diff == 1).astype(np.int))
        bounds = diff.reshape(-1, 1) == np.array([1, -1])
        start, end = np.argwhere(bounds[:, 0]), np.argwhere(bounds[:, 1]) + 1
        runlen = (end - start)[:, 0]
        return np.prod([tribo(l) for l in runlen])



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
