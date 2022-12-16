import functools
import re

import networkx as nx

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = [re.findall(r"([A-Z]{2}|\d+)", line) for line in data.splitlines()]
        rates = {v: int(f) for v, f, *_ in data}
        nz_valves = {v for v, r in rates.items() if r > 0 or v == "AA"}
        nz_valves_idx = {n: i for i, n in enumerate(sorted(nz_valves))}

        g = nx.Graph()
        for v, _, *nxt in data:
            for n in nxt:
                g.add_edge(v, n)

        dists = dict(nx.all_pairs_shortest_path_length(g))
        neigh = {v1: {v2: dists[v1][v2] for v2 in nz_valves if v1 != v2} for v1 in nz_valves}

        @functools.cache
        def dfs(cur, remtime, opened=0):
            if remtime <= 0:
                return 0

            curidx = 1 << nz_valves_idx[cur]
            if opened & curidx:
                return 0

            opened |= curidx
            release = rates[cur] * remtime
            remtime -= 1
            max_release = max(dfs(n, remtime - l, opened) for n, l in neigh[cur].items())
            return max_release + release

        return dfs("AA", 30)



    def solve2(self, data):
        data = [re.findall(r"([A-Z]{2}|\d+)", line) for line in data.splitlines()]
        rates = {v: int(f) for v, f, *_ in data}
        nz_valves = {v for v, r in rates.items() if r > 0}
        nz_valves_idx = {n: i for i, n in enumerate(["AA"] + sorted(nz_valves))}

        g = nx.DiGraph()
        for v, _, *nxt in data:
            for n in nxt:
                g.add_edge(v, n)

        dists = dict(nx.all_pairs_shortest_path_length(g))
        neigh = {v1: {v2: dists[v1][v2] for v2 in nz_valves if v1 != v2} for v1 in nz_valves_idx}

        @functools.cache
        def dfs(cur, remtime, opened=0):
            if remtime <= 0:
                return 0

            curidx = 1 << nz_valves_idx[cur]
            if opened & curidx:
                return 0

            opened |= curidx
            release = rates[cur] * remtime
            remtime -= 1
            max_release = max(dfs(n, remtime - l, opened) for n, l in neigh[cur].items())
            return max_release + release

        assert nz_valves_idx["AA"] == 0
        return max(dfs("AA", 26, visited << 1) + dfs("AA", 26, ~visited << 1) for visited in range(2**(len(nz_valves_idx) - 2)))



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
