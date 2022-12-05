import numpy as np
import scipy.signal as spsig

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = np.array([list(l) for l in data.splitlines()])
        shape = np.array((1,) + data.shape) + 12
        universe = np.zeros(shape, dtype=np.uint8)
        universe[6, 6:6+data.shape[0], 6:6+data.shape[1]] = (data == "#")

        kern = np.ones((3, 3, 3), dtype=universe.dtype)
        kern[1, 1, 1] = 0

        for _ in range(6):
            counts = spsig.convolve(universe, kern, mode="same")
            universe = ((counts == 3) | ((counts == 2) & universe)).astype(dtype=universe.dtype)

        return universe.sum()



    def solve2(self, data):
        data = np.array([list(l) for l in data.splitlines()])
        shape = np.array((1, 1) + data.shape) + 12
        universe = np.zeros(shape, dtype=np.uint8)
        universe[6, 6, 6:6+data.shape[0], 6:6+data.shape[1]] = (data == "#")

        kern = np.ones((3, 3, 3, 3), dtype=universe.dtype)
        kern[1, 1, 1, 1] = 0

        for _ in range(6):
            counts = spsig.convolve(universe, kern, mode="same")
            universe = ((counts == 3) | ((counts == 2) & universe)).astype(dtype=universe.dtype)

        return universe.sum()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
