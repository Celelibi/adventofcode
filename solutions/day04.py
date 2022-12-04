from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        pairs = [[int(v) for r in pair.split(",") for v in r.split("-")] for pair in data.splitlines()]
        pairs = [(set(range(s1, e1 + 1)), set(range(s2, e2 + 1))) for s1, e1, s2, e2 in pairs]
        return sum((s1.issubset(s2) or s1.issuperset(s2)) for s1, s2 in pairs)



    def solve2(self, data):
        pairs = [[int(v) for r in pair.split(",") for v in r.split("-")] for pair in data.splitlines()]
        pairs = [(set(range(s1, e1 + 1)), set(range(s2, e2 + 1))) for s1, e1, s2, e2 in pairs]
        return sum(bool(s1 & s2) for s1, s2 in pairs)



registry.register(str(int(__name__[-2:])), Solver())
