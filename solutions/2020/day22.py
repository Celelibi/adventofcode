import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        p1, p2 = data.split("\n\n")
        p1 = [int(c) for c in p1.splitlines()[1:]]
        p2 = [int(c) for c in p2.splitlines()[1:]]

        while len(p1) > 0 and len(p2) > 0:
            c1, c2 = p1.pop(0), p2.pop(0)
            if c1 > c2:
                p1 += [c1, c2]
            else:
                p2 += [c2, c1]

        return np.arange(len(p1) + len(p2), 0, -1).dot(p1 + p2)



    def solve2(self, data):
        p1, p2 = data.split("\n\n")
        p1 = tuple(int(c) for c in p1.splitlines()[1:])
        p2 = tuple(int(c) for c in p2.splitlines()[1:])

        def play(p1, p2, level=1):
            states = set()
            while len(p1) > 0 and len(p2) > 0:
                if (p1, p2) in states:
                    return True, p1
                states.add((p1, p2))

                c1, p1, c2, p2 = p1[0], p1[1:], p2[0], p2[1:]
                if len(p1) >= c1 and len(p2) >= c2:
                    p1win, _ = play(p1[:c1], p2[:c2], level + 1)
                else:
                    p1win = c1 > c2

                if p1win:
                    p1 += (c1, c2)
                else:
                    p2 += (c2, c1)

            return len(p1) > 0, p1 + p2

        _, winnerdeck = play(p1, p2)
        return np.arange(len(winnerdeck), 0, -1).dot(winnerdeck)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
