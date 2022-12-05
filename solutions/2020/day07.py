import re

import networkx as nx

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def build_graph(self, data):
        r = re.compile(r'(.*) bags contain (.*)')
        rc = re.compile(r'(\d+) ([^,]*) bags?')
        g = nx.DiGraph()

        for line in data.splitlines():
            container, contained = r.match(line).groups()

            if contained == "no other bags":
                g.add_node(container)
                continue

            for m in rc.finditer(contained):
                g.add_edge(m.group(2), container, n=int(m.group(1)))

        return g



    def solve1(self, data):
        g = nx.transitive_closure(self.build_graph(data))
        return len(g.adj["shiny gold"])



    def solve2(self, data):
        g = self.build_graph(data).reverse()
        def count(node):
            return sum((count(n) + 1) * g.edges[node, n]["n"] for n in g.adj[node])
        return count("shiny gold")



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
