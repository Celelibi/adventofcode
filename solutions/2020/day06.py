import sklearn.preprocessing as skpre

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        return sum(len(set(g.replace("\n", ""))) for g in data.split("\n\n"))



    def solve2(self, data):
        data = data.split("\n\n")
        mlb = skpre.MultiLabelBinarizer()
        return sum(mlb.fit_transform(g.splitlines()).prod(axis=0).sum() for g in data)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
