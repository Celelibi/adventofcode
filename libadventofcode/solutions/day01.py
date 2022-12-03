from . import base
from .. import registry



class Solver(base.Solver):
    def solve1(self, data):
        elves = [sum(int(food) for food in e.split()) for e in data.split("\n\n")]
        return max(elves)



    def solve2(self, data):
        elves = [sum(int(food) for food in e.split()) for e in data.split("\n\n")]
        return sum(sorted(elves, reverse=True)[:3])



registry.register("1", Solver())
