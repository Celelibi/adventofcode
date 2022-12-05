import re
import numpy as np
import scipy.signal as spsig

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.splitlines()
        r = re.compile(r'([ns]?[ew])')

        dirs = {
            "e": np.array([2, 0]),
            "w": np.array([-2, 0]),
            "ne": np.array([1, 1]),
            "nw": np.array([-1, 1]),
            "se": np.array([1, -1]),
            "sw": np.array([-1, -1])
        }

        blackcells = set()
        for tile in data:
            coord = sum(dirs[d] for d in r.findall(tile))
            blackcells ^= {tuple(coord)}

        return len(blackcells)



    def solve2(self, data):
        data = data.splitlines()
        r = re.compile(r'([ns]?[ew])')

        dirs = {
            "e": np.array([0, 1]),
            "w": np.array([0, -1]),
            "ne": np.array([-1, 0]),
            "nw": np.array([-1, -1]),
            "se": np.array([1, 1]),
            "sw": np.array([1, 0])
        }

        width = 2 * max(len(tile) for tile in data) + 1 + 2 * 100
        isblack = np.zeros((width, width), dtype=np.bool)

        for tile in data:
            coord = sum(dirs[d] for d in r.findall(tile))
            isblack[tuple(coord)] ^= 1

        kern = np.ones((3, 3), dtype=np.int) - np.eye(3, dtype=np.int)[:, ::-1]

        for _ in range(100):
            counts = spsig.convolve2d(isblack, kern, mode='same', boundary='wrap')
            isblack = (isblack & (counts != 0) & (counts <= 2)) | (counts == 2)

        return isblack.sum()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
