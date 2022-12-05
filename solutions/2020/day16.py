import re
import numpy as np
from scipy.sparse import csr_matrix as spcsr
import networkx as nx

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        rules, myticket, tickets = data.split("\n\n")
        tickets = tickets.splitlines()[1:]
        tickets = np.array([t.split(",") for t in tickets], dtype=np.int)

        rr = re.compile(r'.*: (\d+)-(\d+) or (\d+)-(\d+)')
        rules = [rr.search(l).groups() for l in rules.splitlines()]
        rules = np.array(rules, dtype=np.int)

        allowedvals = np.zeros(max(rules.max(), tickets.max()) + 1, dtype=np.bool)
        for r in rules:
            allowedvals[r[0]:r[1]] = True
            allowedvals[r[2]:r[3]] = True

        invalidvalues = tickets[~allowedvals[tickets]]
        return invalidvalues.sum()



    def solve2(self, data):
        rules, myticket, tickets = data.split("\n\n")
        myticket = np.array(myticket.splitlines()[1].split(","), dtype=np.int)
        tickets = tickets.splitlines()[1:]
        tickets = np.array([t.split(",") for t in tickets], dtype=np.int)

        rr = re.compile(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)')
        rules = np.array([rr.search(l).groups() for l in rules.splitlines()])
        names, rules = rules[:, 0], rules[:, 1:].astype(np.int)

        allowedvals = np.zeros(max(rules.max(), tickets.max()) + 1, dtype=np.bool)
        for r in rules:
            allowedvals[r[0]:r[1]] = True
            allowedvals[r[2]:r[3]] = True

        tickets = tickets[np.sum(~allowedvals[tickets], axis=1) == 0]
        rt = rules.T.reshape(4, -1, 1, 1)
        valid = (tickets >= rt[0]) & (tickets <= rt[1]) | (tickets >= rt[2]) & (tickets <= rt[3])
        candidates = ~(~valid).sum(axis=1).astype(np.bool)

        g = nx.bipartite.from_biadjacency_matrix(spcsr(candidates), create_using=nx.DiGraph)
        rename = dict(zip((n for n, at in g.nodes.data() if at["bipartite"] == 0), names))
        rename |= dict(zip((n for n, at in g.nodes.data() if at["bipartite"] == 1), range(tickets.shape[1])))
        g = nx.relabel_nodes(g, rename)

        g.add_edges_from([("Source", n, {"capacity": 1}) for n in names])
        g.add_edges_from([(n, "Sink", {"capacity": 1}) for n in range(tickets.shape[1])])
        res = nx.max_flow_min_cost(g, "Source", "Sink")

        fields = {n: k for n in names for k, v in res[n].items() if v == 1}
        departurefields = [v for k, v in fields.items() if k.startswith("departure")]

        return myticket[departurefields].prod()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
