import numpy as np

from libadventofcode import base
from libadventofcode import registry



def sliding_window(a, width=3):
    idxrow = np.arange(a.shape[0] - width + 1)
    idxcol = np.arange(width)
    idx = idxrow.reshape(-1 ,1) + idxcol
    return a[idx]



def firstnonsum(data):
    mat = sliding_window(data, 25)[:-1, :]
    a = mat.reshape(-1, 25, 1)
    b = mat.reshape(-1, 1, 25)
    issum = (a + b == data[25:].reshape(-1, 1, 1))
    r = np.arange(25)
    issum[:, r, r] = False
    cantwriteassum = ~issum.sum(axis=(1, 2), dtype=np.bool)
    idx, = cantwriteassum.nonzero()
    return data[25 + idx[0]]



class Solver(base.Solver):
    def solve1(self, data):
        data = np.array(data.splitlines(), dtype=np.int)
        return firstnonsum(data)



    def solve2(self, data):
        data = np.array(data.splitlines(), dtype=np.int)
        target = firstnonsum(data)
        cs = data.cumsum()
        iscontsum = (cs.reshape(-1, 1) - cs == target)
        r = np.arange(len(iscontsum) - 1)
        iscontsum[r + 1, r] = False
        [(e, b)] = np.argwhere(iscontsum)
        assert data[b+1:e+1].sum() == target
        return data[b+1:e+1].min() + data[b+1:e+1].max()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
