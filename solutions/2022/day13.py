import functools

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    @staticmethod
    def cmp(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return a - b
        if isinstance(a, int):
            return Solver.cmp([a], b)
        if isinstance(b, int):
            return Solver.cmp(a, [b])
        for va, vb in zip(a, b):
            if res := Solver.cmp(va, vb):
                return res
        return len(a) - len(b)



    def solve1(self, data):
        pairs = [[eval(packet) for packet in pair.splitlines()] for pair in data.split("\n\n")]
        return sum(i + 1 for i, (l, r) in enumerate(pairs) if self.cmp(l, r) <= 0)



    def solve2(self, data):
        packets = [eval(packet) for packet in data.splitlines() if packet] + [[[2]], [[6]]]
        packets.sort(key=functools.cmp_to_key(self.cmp))
        return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
