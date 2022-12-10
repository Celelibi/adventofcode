import subprocess

import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        insts = [inst.split(" ") for inst in data.splitlines()]
        xs = [1]
        for inst, *values in insts:
            if inst.startswith("noop"):
                xs.append(xs[-1])
            if inst.startswith("addx"):
                xs += [xs[-1], xs[-1] + int(values[0])]

        return sum(xs[i - 1] * i for i in (20, 60, 100, 140, 180, 220))



    def solve2(self, data):
        insts = [inst.split(" ") for inst in data.splitlines()]
        xs = [1]
        for inst, *values in insts:
            if inst.startswith("noop"):
                xs.append(xs[-1])
            if inst.startswith("addx"):
                xs += [xs[-1], xs[-1] + int(values[0])]

        xs = np.array(xs[:-1]).reshape(-1, 40)
        clocks = np.tile(np.arange(40), (6, 1))
        crt = (xs >= clocks - 1) & (xs < clocks + 2)

        img = b"P1\n%d %d\n" % (*reversed(crt.shape),)
        img += b"".join(str(c).encode() for row in crt.astype(int) for c in row)

        res = subprocess.run(["gocr", "-i", "-"], input=img, capture_output=True)
        return res.stdout.decode().rstrip()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
