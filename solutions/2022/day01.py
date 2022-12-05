from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        elves = [sum(int(food) for food in e.split()) for e in data.split("\n\n")]
        return max(elves)



    def solve2(self, data):
        elves = [sum(int(food) for food in e.split()) for e in data.split("\n\n")]
        return sum(sorted(elves, reverse=True)[:3])



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
