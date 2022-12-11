import math
import re

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve(self, data, rounds, relief=3):
        r = re.compile(r"""Monkey .*:
  Starting items: (?P<items>.*)
  Operation: new = (?P<op>.*)
  Test: divisible by (?P<div>.*)
    If true: throw to monkey (?P<iftrue>.*)
    If false: throw to monkey (?P<iffalse>.*)""")

        monkeys = []
        for rule in data.split("\n\n"):
            m = r.match(rule).groupdict()
            m["items"] = [int(i) for i in m["items"].split(", ")]
            m.update({k: int(m[k]) for k in ("div", "iftrue", "iffalse")})
            monkeys.append(m)

        proddiv = math.prod([m["div"] for m in monkeys])

        business = [0] * len(monkeys)

        for _ in range(rounds):
            for i, m in enumerate(monkeys):
                business[i] += len(m["items"])

                for item in m["items"]:
                    new = eval(m["op"], {"old": item}) // relief % proddiv
                    if new % m["div"] == 0:
                        monkeys[m["iftrue"]]["items"].append(new)
                    else:
                        monkeys[m["iffalse"]]["items"].append(new)

                m["items"] = []

        return math.prod(sorted(business)[-2:])



    def solve1(self, data):
        return self.solve(data, 20)



    def solve2(self, data):
        return self.solve(data, 10000, 1)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
