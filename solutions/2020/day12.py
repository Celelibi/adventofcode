import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.splitlines()
        pos = np.array([0, 0])
        curdir = 0

        card = {d: n for n, d in enumerate("ESWN")}
        offsets = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]])

        for l in data:
            inst, val = l[0], int(l[1:])
            if inst in card:
                pos += offsets[card[inst]] * val
            elif inst == "F":
                pos += offsets[curdir] * val
            elif inst == "R":
                curdir = (curdir + val // 90) % 4
            elif inst == "L":
                curdir = (curdir - val // 90) % 4
            else:
                raise ValueError("Unexpected instruction: " + l)

        return abs(pos).sum()



    def solve2(self, data):
        data = data.splitlines()

        card = {d: n for n, d in enumerate("ESWN")}
        offsets = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]])
        rot = {"R": np.array([[0, 1], [-1, 0]]), "L": np.array([[0, -1], [1, 0]])}

        pos = np.array([0, 0])
        way = 10 * offsets[card["E"]] + 1 * offsets[card["N"]]

        for l in data:
            inst, val = l[0], int(l[1:])
            if inst in card:
                way += offsets[card[inst]] * val
            elif inst == "F":
                pos += way * val
            elif inst in rot:
                way = np.linalg.matrix_power(rot[inst], val // 90).dot(way)
            else:
                raise ValueError("Unexpected instruction: " + l)

        return abs(pos).sum()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
