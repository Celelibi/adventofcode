import subprocess

import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        insts = [[1, 0] if inst == "noop" else [2, inst.split(" ")[1]] for inst in data.splitlines()]
        insts = np.array([[1, 1]] + insts, dtype=int)

        xs = np.repeat(insts[:-1, 1].cumsum(), insts[1:, 0])
        idx = np.arange(6) * 40 + 20
        return (xs[idx - 1] * idx).sum()



    def solve2(self, data):
        insts = [[1, 0] if inst == "noop" else [2, inst.split(" ")[1]] for inst in data.splitlines()]
        insts = np.array([[1, 1]] + insts, dtype=int)

        xs = np.repeat(insts[:-1, 1].cumsum(), insts[1:, 0]).reshape(-1, 40)
        clocks = np.tile(np.arange(40), (6, 1))
        crt = (xs >= clocks - 1) & (xs < clocks + 2)

        img = b"P1\n%d %d\n" % (*reversed(crt.shape),)
        img += b"".join(str(c).encode() for row in crt.astype(int) for c in row)

        res = subprocess.run(["gocr", "-i", "-"], input=img, capture_output=True)
        return res.stdout.decode().rstrip()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
