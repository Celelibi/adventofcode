import string

from . import base
from .. import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = [(set(line[:len(line) // 2]) & set(line[len(line) // 2:])).pop() for line in data.split()]
        return sum(string.ascii_letters.index(c) + 1 for c in data)



    def solve2(self, data):
        data = [set(line) for line in data.split()]
        badges = [(data[i] & data[i + 1] & data[i + 2]).pop() for i in range(0, len(data), 3)]
        return sum(string.ascii_letters.index(c) + 1 for c in badges)



registry.register("3", Solver())
