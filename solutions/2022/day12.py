import string

import networkx as nx
import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    @staticmethod
    def parse_graph(data):
        heights = "S" + string.ascii_lowercase + "E"
        grid = np.array([[heights.index(c) for c in line] for line in data.splitlines()])
        start, = np.argwhere(grid == heights.index("S"))
        end, = np.argwhere(grid == heights.index("E"))

        grid[grid == heights.index("S")] = heights.index("a")
        grid[grid == heights.index("E")] = heights.index("z")

        g = nx.DiGraph()
        for y in range(grid.shape[0]):
            for x in range(grid.shape[1]):

                if y < grid.shape[0] - 1:
                    if grid[y + 1][x] <= grid[y][x] + 1:
                        g.add_edge((y, x), (y + 1, x))

                    if grid[y + 1][x] + 1 >= grid[y][x]:
                        g.add_edge((y + 1, x), (y, x))

                if x < grid.shape[1] - 1:
                    if grid[y][x + 1] <= grid[y][x] + 1:
                        g.add_edge((y, x), (y, x + 1))

                    if grid[y][x + 1] + 1 >= grid[y][x]:
                        g.add_edge((y, x + 1), (y, x))

        return grid, tuple(start), tuple(end), g



    def solve1(self, data):
        _, start, end, g = self.parse_graph(data)
        return nx.shortest_path_length(g, source=start, target=end)



    def solve2(self, data):
        grid, start, end, g = self.parse_graph(data)

        sources = [tuple(c) for c in np.argwhere(grid == grid[start])]
        return nx.multi_source_dijkstra_path_length(g, sources=sources)[end]



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
