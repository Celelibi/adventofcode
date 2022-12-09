import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        def visible_from_top(grid):
            grid = np.pad(grid, ((1, 0), (0, 0)), constant_values=-1)
            runmax = np.maximum.accumulate(grid, axis=0)
            return (np.diff(runmax, axis=0) > 0)

        data = data.splitlines()
        data = np.array([list(line) for line in data], dtype=int)

        visible = visible_from_top(data)
        visible |= visible_from_top(data[::-1])[::-1]
        visible |= visible_from_top(data.T).T
        visible |= visible_from_top(data.T[::-1])[::-1].T

        return visible.sum()



    def solve2(self, data):
        def scenic_score_down(grid):
            scores = np.zeros_like(grid)
            for y0 in range(grid.shape[0]):
                for x0 in range(grid.shape[1]):
                    s = 0
                    for y in range(y0 + 1, grid.shape[0]):
                        scores[y0, x0] += 1
                        if grid[y, x0] >= grid[y0, x0]:
                            break
            return scores

        data = data.splitlines()
        data = np.array([list(line) for line in data], dtype=int)
        scores = scenic_score_down(data)
        scores *= scenic_score_down(data[::-1])[::-1]
        scores *= scenic_score_down(data.T).T
        scores *= scenic_score_down(data.T[::-1])[::-1].T

        return scores.max()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
