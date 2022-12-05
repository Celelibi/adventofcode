import numpy as np

from libadventofcode import base
from libadventofcode import registry


def chinese(rem, mod):
    N = mod.prod()
    Nh = N // mod
    inv = np.array([pow(int(nh), -1, int(n)) for n, nh in zip(mod, Nh)])
    return rem.dot(inv * Nh) % N



class Solver(base.Solver):
    def solve1(self, data):
        date, buses = data.splitlines()
        date = int(date)
        buses = np.array([int(b) for b in buses.split(",") if b != "x"])
        waittime = buses - date % buses
        idx = waittime.argmin()
        return buses[idx] * waittime[idx]



    def solve2(self, data):
        _, buses = data.splitlines()
        buses = np.array([(i, int(b)) for i, b in enumerate(buses.split(",")) if b != "x"])
        offsets, periods = buses.T
        return chinese(-offsets, periods)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
