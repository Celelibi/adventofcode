import re

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = data.replace("*", "-")

        class I:
            def __init__(self, v):
                self.v = v
            def __add__(a, b):
                return I(a.v + b.v)
            def __sub__(a, b):
                return I(a.v * b.v)

        data = re.sub(r'(\d+)', 'I(\\1)', data)
        return sum(eval(l, {"I": I}).v for l in data.splitlines())


    def solve2(self, data):
        data = data.replace("*", "-").replace("+", "*").replace("-", "+")

        class I:
            def __init__(self, v):
                self.v = v
            def __add__(a, b):
                return I(a.v * b.v)
            def __mul__(a, b):
                return I(a.v + b.v)

        data = re.sub(r'(\d+)', 'I(\\1)', data)
        return sum(eval(l, {"I": I}).v for l in data.splitlines())



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
