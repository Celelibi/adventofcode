import math
import re

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve(self, data, rounds, relief=3):
        r = re.compile(r"""Monkey .*:
  Starting items: (.*)
  Operation: new = (.*)
  Test: divisible by (.*)
    If true: throw to monkey (.*)
    If false: throw to monkey (.*)""")

        rules = []
        hold = []
        for rule in data.split("\n\n"):
            m = r.match(rule)
            hold.append([int(i) for i in m.group(1).split(", ")])
            op, div, iftrue, iffalse = m.group(2, 3, 4, 5)
            div, iftrue, iffalse = int(div), int(iftrue), int(iffalse)
            rules.append((op, div, iftrue, iffalse))

        proddiv = math.prod([div for _, div, _, _ in rules])

        business = [0] * len(rules)
        for _ in range(rounds):
            for monkey, (items, (op, div, iftrue, iffalse)) in enumerate(zip(hold, rules)):
                hold[monkey] = []
                business[monkey] += len(items)
                for item in items:
                    new = eval(op, {"old": item}) // relief % proddiv
                    hold[iftrue if new % div == 0 else iffalse].append(new)

        return math.prod(sorted(business)[-2:])



    def solve1(self, data):
        return self.solve(data, 20)



    def solve2(self, data):
        return self.solve(data, 10000, 1)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
