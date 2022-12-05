import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        cups = [int(c) for c in data.rstrip()]
        for _ in range(100):
            current = cups.pop(0)
            picksup, cups = cups[:3], cups[3:]

            dest = current
            destidx = None
            while destidx is None:
                dest = (dest - 2) % 9 + 1
                try:
                    destidx = cups.index(dest)
                except ValueError:
                    pass

            cups[destidx+1:destidx+1] = picksup
            cups.append(current)

        oneidx = cups.index(1)
        return "".join(str(x) for x in cups[oneidx+1:] + cups[:oneidx])



    def solve2(self, data):
        cups = [int(c) for c in data.rstrip()]
        nextcup = np.arange(1, 1000002)
        nextcup[cups] = cups[1:] + [len(cups) + 1]
        nextcup[[0, -1]] = [0, cups[0]]

        current = cups[0]
        for _ in range(10000000):
            picksup = []
            pu = current
            for _ in range(3):
                pu = nextcup[pu]
                picksup.append(pu)

            dest = (current - 2) % (len(nextcup) - 1) + 1
            while dest in picksup:
                dest = (dest - 2) % (len(nextcup) - 1) + 1

            nextcup[current] = nextcup[picksup[-1]]
            nextcup[picksup[-1]] = nextcup[dest]
            nextcup[dest] = picksup[0]
            current = nextcup[current]

        return nextcup[1] * nextcup[nextcup[1]]



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
