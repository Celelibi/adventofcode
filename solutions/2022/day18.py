import numpy as np
from skimage import segmentation as skseg

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        coord = np.array([line.split(",") for line in data.splitlines()], dtype=int)
        grid = np.zeros(coord.max(axis=0) + 3, dtype=int)
        grid[tuple(coord.T + 1)] = 1
        return sum((np.diff(grid, axis=a) != 0).sum() for a in range(3))




    def solve2(self, data):
        coord = np.array([line.split(",") for line in data.splitlines()], dtype=int)
        grid = np.zeros(coord.max(axis=0) + 3, dtype=int)
        grid[tuple(coord.T + 1)] = 1
        skseg.flood_fill(grid, (0, 0, 0), 3, connectivity=1, in_place=True)
        return sum((np.abs(np.diff(grid, axis=a)) > 1).sum() for a in range(3))



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
