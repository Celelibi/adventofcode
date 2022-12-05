import re
import numpy as np
import scipy.sparse as spsparse
import networkx as nx
import sklearn.preprocessing as skpre

from libadventofcode import base
from libadventofcode import registry



def make_bipartite(mat, names0, names1, **kwargs):
    g = nx.bipartite.from_biadjacency_matrix(spsparse.csr_matrix(mat), **kwargs)
    rename = dict(zip((n for n, at in g.nodes.data() if at["bipartite"] == 0), names0))
    rename |= dict(zip((n for n, at in g.nodes.data() if at["bipartite"] == 1), names1))
    return nx.relabel_nodes(g, rename)



class Solver(base.Solver):
    def solve1(self, data):
        r = re.compile(r'(.*) \(contains (.*)\)')
        data = [r.match(l).groups() for l in data.splitlines()]
        ings = [ings.split() for ings, als in data]
        als = [als.split(", ") for ings, als in data]

        mlbing = skpre.MultiLabelBinarizer()
        mlbals = skpre.MultiLabelBinarizer()
        recipesoh = mlbing.fit_transform(ings).astype(np.bool)
        allergensoh = mlbals.fit_transform(als).astype(np.bool)

        recipesal = np.ones((len(mlbals.classes_),) + recipesoh.shape, dtype=np.bool)
        for i, (al, roh) in enumerate(zip(allergensoh, recipesoh)):
            recipesal[al, i] = roh

        # Ingredients that may be the allergen for each allergen
        maybeal = recipesal.prod(axis=1)
        # Definitely not allergen
        noal = (maybeal.sum(axis=0) == 0)
        return recipesoh[:, noal].sum()



    def solve2(self, data):
        r = re.compile(r'(.*) \(contains (.*)\)')
        data = [r.match(l).groups() for l in data.splitlines()]
        ings = [ings.split() for ings, als in data]
        als = [als.split(", ") for ings, als in data]

        mlbing = skpre.MultiLabelBinarizer()
        mlbals = skpre.MultiLabelBinarizer()
        recipesoh = mlbing.fit_transform(ings).astype(np.bool)
        allergensoh = mlbals.fit_transform(als).astype(np.bool)

        recipesal = np.ones((len(mlbals.classes_),) + recipesoh.shape, dtype=np.bool)
        for i, (al, roh) in enumerate(zip(allergensoh, recipesoh)):
            recipesal[al, i] = roh

        # Ingredients that may be the allergen for each allergen
        maybeal = recipesal.prod(axis=1)
        # Definitely allergen
        aling = (maybeal.sum(axis=0) > 0)

        alnames = mlbals.classes_
        ingnames = mlbing.classes_[aling]
        g = make_bipartite(maybeal[:, aling], alnames, ingnames, create_using=nx.DiGraph)
        g.add_edges_from([("Source", n, {"capacity": 1}) for n in alnames])
        g.add_edges_from([(n, "Sink", {"capacity": 1}) for n in ingnames])
        res = nx.max_flow_min_cost(g, "Source", "Sink")

        return ",".join(ing for al in sorted(alnames) for ing in res[al] if res[al][ing])



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
