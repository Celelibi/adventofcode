import numpy as np

from . import base
from .. import registry



class Solver(base.Solver):
    parse1 = {"A": 0, "B": 1, "C": 2, "X": 0, "Y": 1, "Z": 2}
    parse2 = {"A": 0, "B": 1, "C": 2, "X": 2, "Y": 0, "Z": 1}
    choice_value = np.array([1, 2, 3])
    win_value = np.array([3, 6, 0])

    def solve1(self, data):
        data = [rnd.split() for rnd in data.splitlines()]
        data = np.array([(self.parse1[a], self.parse1[b]) for a, b in data])
        win = (data[:, 1] - data[:, 0]) % 3
        return (self.choice_value[data[:, 1]] + self.win_value[win]).sum()



    def solve2(self, data):
        data = [rnd.split() for rnd in data.splitlines()]
        data = np.array([(self.parse2[a], self.parse2[b]) for a, b in data])
        mychoice = (data[:, 1] + data[:, 0]) % 3
        return (self.choice_value[mychoice] + self.win_value[data[:, 1]]).sum()



registry.register("2", Solver())
