import re

import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = [re.findall(r"(\d+),(\d+)", line) for line in data.splitlines()]
        rox = np.array([s + e for path in data for s, e in zip(path, path[1:])], dtype=int)

        # Shift the coordinates to reasonable values
        sandbox_end = rox.reshape(-1, 2).max(axis=0) + [2, 1]
        sandbox_start = np.array([rox.reshape(-1, 2)[:, 0].min() - 1, 0])
        rox.reshape(-1, 2)[:, :] -= sandbox_start

        sandbox = np.zeros(sandbox_end[::-1] - sandbox_start[::-1], dtype=int)
        for xmin, ymin, xmax, ymax in rox:
            xmin, xmax = sorted([xmin, xmax])
            ymin, ymax = sorted([ymin, ymax])
            sandbox[ymin:ymax + 1, xmin:xmax + 1] = 1

        while True:
            x, y = [500, 0] - sandbox_start

            while True:
                next_rocks, = np.nonzero(sandbox[y:, x])
                if not len(next_rocks):
                    return (sandbox == 2).sum()

                y += next_rocks[0]
                if not sandbox[y, x - 1]:
                    x -= 1
                elif not sandbox[y, x + 1]:
                    x += 1
                else:
                    sandbox[y - 1, x] = 2
                    break



    def solve2(self, data):
        data = [re.findall(r"(\d+),(\d+)", line) for line in data.splitlines()]
        rox = np.array([s + e for path in data for s, e in zip(path, path[1:])], dtype=int)

        max_x, max_y = rox.reshape(-1, 2).max(axis=0)
        min_x, min_y = rox.reshape(-1, 2)[:, 0].min(), 0
        sandbox_start = np.array([min(min_x, 500 - max_y - 2) - 1, min_y])
        sandbox_end = np.array([max(max_x, 500 + max_y + 2) + 1, max_y + 3])
        rox.reshape(-1, 2)[:, :] -= sandbox_start

        sandbox = np.zeros(sandbox_end[::-1] - sandbox_start[::-1], dtype=int)
        sandbox[-1, :] = True
        for xmin, ymin, xmax, ymax in rox:
            xmin, xmax = sorted([xmin, xmax])
            ymin, ymax = sorted([ymin, ymax])
            sandbox[ymin:ymax + 1, xmin:xmax + 1] = 1

        source = [500, 0] - sandbox_start
        stack = [source] # List of coords we know the path of
        while True:
            if sandbox[source[1], source[0]]:
                return (sandbox == 2).sum()

            x, y = stack.pop()
            while True:
                stack.append((x, y))

                y += 1
                if not sandbox[y, x]:
                    continue

                if not sandbox[y, x - 1]:
                    x -= 1
                elif not sandbox[y, x + 1]:
                    x += 1
                else:
                    sandbox[y - 1, x] = 2
                    stack.pop()
                    break



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
