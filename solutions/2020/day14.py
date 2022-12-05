import itertools as it
import re

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.splitlines()
        rmask = re.compile(r'mask = ([01X]*)')
        rmem = re.compile(r'mem\[(\d+)\] = (\d+)')

        mem = {}

        for l in data:
            mmask = rmask.match(l)
            mmem = rmem.match(l)

            if mmask is not None:
                mask = mmask.group(1)
                maskset = int(mask.replace("X", "0"), 2)
                maskunset = int(mask.replace("X", "1"), 2)
            elif mmem is not None:
                idx, val = mmem.groups()
                mem[int(idx)] = (int(val) | maskset) & maskunset
            else:
                raise ValueError("Can't parse line: %r" % l)

        return sum(mem.values())


    def solve2(self, data):
        data = data.splitlines()
        rmask = re.compile(r'mask = ([01X]*)')
        rmem = re.compile(r'mem\[(\d+)\] = (\d+)')

        mem = {}

        for l in data:
            mmask = rmask.match(l)
            mmem = rmem.match(l)

            if mmask is not None:
                mask = mmask.group(1)
                maskset = int(mask.replace("X", "0"), 2)
                floats = set(35 - i for i, b in enumerate(mask) if b == "X")
            elif mmem is not None:
                idx, val = mmem.groups()
                idx = int(idx) | maskset
                floatsunset = ~sum(1 << i for i in floats)
                for n in range(len(floats) + 1):
                    for fbits in it.combinations(floats, n):
                        addr = (idx & floatsunset) | sum(1 << i for i in fbits)
                        mem[addr] = int(val)
            else:
                raise ValueError("Can't parse line: %r" % l)

        return sum(mem.values())



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
