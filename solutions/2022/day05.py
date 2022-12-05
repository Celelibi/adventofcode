import re

import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        stacks, moves = data.split("\n\n")
        stacks = np.array([list(line) for line in stacks.splitlines()]).T[1::4, -2::-1]
        stacks = [list("".join(line).rstrip()) for line in stacks]

        for move in moves.splitlines():
            m = re.match(r'move (\d+) from (\d+) to (\d+)', move)
            n, f, t = int(m.group(1)), int(m.group(2)) - 1, int(m.group(3)) - 1

            for _ in range(n):
                stacks[t].append(stacks[f].pop(-1))

        return "".join([stack[-1] for stack in stacks])



    def solve2(self, data):
        stacks, moves = data.split("\n\n")
        stacks = np.array([list(line) for line in stacks.splitlines()]).T[1::4, -2::-1]
        stacks = [list("".join(line).rstrip()) for line in stacks]

        for move in moves.splitlines():
            m = re.match(r'move (\d+) from (\d+) to (\d+)', move)
            n, f, t = int(m.group(1)), int(m.group(2)) - 1, int(m.group(3)) - 1

            stacks[t] += stacks[f][-n:]
            stacks[f] = stacks[f][:-n]

        return "".join([stack[-1] for stack in stacks])



registry.register(str(int(__name__[-2:])), Solver())
