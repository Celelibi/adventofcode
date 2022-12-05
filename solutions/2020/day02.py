import re

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        r = re.compile(r'(\d+)-(\d+) (.): (.*)')
        data = data.splitlines()

        data = [r.match(line).groups() for line in data]
        res = 0
        for mi, ma, c, pwd in data:
            if pwd.count(c) in range(int(mi), int(ma) + 1):
                res += 1

        return res



    def solve2(self, data):
        r = re.compile(r'(\d+)-(\d+) (.): (.*)')
        data = data.splitlines()

        data = [r.match(line).groups() for line in data]
        res = 0
        for idx1, idx2, c, pwd in data:
            if (pwd[int(idx1)-1] == c) ^ (pwd[int(idx2)-1] == c):
                res += 1

        return res



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
