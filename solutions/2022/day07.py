from collections import defaultdict

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    @staticmethod
    def parse_sizes(data):
        cwd = None
        sizes = defaultdict(lambda: 0)

        for line in data.splitlines():
            if line == "$ cd /":
                cwd = []
            elif line == "$ cd ..":
                cwd.pop()
            elif line.startswith("$ cd"):
                cwd.append(line.split(" ", 2)[2])

            if not line.startswith(("$", "dir")):
                for i in range(len(cwd) + 1):
                    sizes[tuple(cwd[:i])] += int(line.split(" ")[0])

        return sizes.values(), sizes[()]



    def solve1(self, data):
        return sum(v for v in self.parse_sizes(data)[0] if v <= 100000)



    def solve2(self, data):
        sizes, total_size = self.parse_sizes(data)
        to_free = total_size - (70_000_000 - 30_000_000)
        return min(s for s in sizes if s >= to_free)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
