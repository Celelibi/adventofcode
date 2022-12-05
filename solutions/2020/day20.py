from collections import defaultdict
import math
import numpy as np
import scipy.signal as spsig

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        tiles = [t.splitlines() for t in data.split("\n\n")][:-1]
        ids = np.array([int(t[0][5:-1]) for t in tiles])
        tiles = np.array([[list(l) for l in t[1:]] for t in tiles])
        tiles = (tiles == "#")
        width = tiles.shape[-1]

        w = np.logspace(0, width - 1, width, base=2, dtype=np.int)
        tb = tiles[:, [0, -1], :]
        lr = tiles[:, :, [0, -1]].transpose(0, 2, 1)
        edges = np.concatenate((tb, lr), axis=1)
        edges = np.minimum(edges.dot(w), edges.dot(w[::-1]))

        et = defaultdict(list)
        for i, es in enumerate(edges):
            for e in es:
                et[e].append(i)

        lonelyedge = set(e for e, t in et.items() if len(t) < 2)
        bordertiles = np.array([t for e in lonelyedge for t in et[e]])
        bordertiles, counts = np.unique(bordertiles, return_counts=True)

        return ids[bordertiles[counts > 1]].prod()



    def solve2(self, data):
        tiles = [t.splitlines() for t in data.split("\n\n")][:-1]
        ids = np.array([int(t[0][5:-1]) for t in tiles])
        tiles = np.array([[list(l) for l in t[1:]] for t in tiles])
        tiles = (tiles == "#")
        width = tiles.shape[-1]

        w = np.logspace(0, width - 1, width, base=2, dtype=np.int)
        t, r, b, l = tiles[:, 0, :], tiles[:, :, -1], tiles[:, -1, ::-1], tiles[:, ::-1, 0]
        sedges = np.stack((t, r, b, l), axis=1)
        t, r, b, l = tiles[:, 0, ::-1], tiles[:, :, 0], tiles[:, -1, :], tiles[:, ::-1, -1]
        redges = np.stack((t, r, b, l), axis=1)
        edges = np.stack((sedges, redges), axis=1)
        edges = edges.dot(w)
        #edges = edges.min(axis=1)

        et = defaultdict(list)
        for tileidx, sr in enumerate(edges):
            for es, rev in zip(sr, [0, 1]):
                for sideid, e in enumerate(es):
                    et[e].append((tileidx, rev, sideid))

        edgeusecnt = np.array([len(et[e]) if e in et else 0 for e in range(edges.max() + 1)])
        lonelyedge = np.flatnonzero(edgeusecnt == 1)
        bordertiles = np.array([t for e in lonelyedge for t, r, s in et[e]])
        bordertiles, counts = np.unique(bordertiles, return_counts=True)

        mapsize = math.isqrt(tiles.shape[0])
        image = np.zeros([mapsize, mapsize] * (np.array(tiles.shape[1:]) - 2), dtype=np.int)

        cornersidx = bordertiles[counts > 2]
        corner = cornersidx.min()
        cornerlonelyedges = (edgeusecnt[edges[corner, 0]] == 1)
        rotcorner = {0b1001: 0, 0b1100: 1, 0b0110: 2, 0b0011: 3}
        s = rotcorner[cornerlonelyedges.dot([8, 4, 2, 1])]

        def nexttile(e, prev=None):
            return next((t, r, s) for t, r, s in et[e] if t != prev)

        def revedge(e):
            return int(bin(e)[:1:-1].ljust(tiles.shape[-1], "0"), 2)

        northedge = edges[corner, 0, s]
        prevnorthtile = None

        for i in range(mapsize):
            t, r, s = nexttile(northedge, prevnorthtile)
            westedge = edges[t, r, (s + 3) % 4]
            northedge = revedge(edges[t, r, (s + 2) % 4])
            prevnorthtile = t
            prevwesttile = None

            for j in range(mapsize):
                t, r, s = nexttile(westedge, prevwesttile)
                westedge = revedge(edges[t, r, (2 + s) % 4])
                prevwesttile = t

                tile = np.rot90(tiles[t, :, ::-1] if r else tiles[t], k=1 + s)[1:-1, 1:-1]
                h, w = tile.shape
                image[i * h:(i + 1) * h, j * w:(j + 1) * w] = tile

        kernel = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
        kernel = np.array([list(line) for line in kernel.splitlines()])
        kernel = (kernel == "#")

        def findsymmetry(img, kern):
            s = kern.sum()
            for r in range(4):
                if spsig.convolve2d(np.rot90(img, k=r), kern, mode='valid').max() == s:
                    return r, 0
                if spsig.convolve2d(np.rot90(img[:, ::-1], k=r), kern, mode='valid').max() == s:
                    return r, 1
            raise ValueError

        r, s = findsymmetry(image, kernel)
        image = np.rot90(image[:, ::-1] if s else image, k=r)
        conv = spsig.convolve2d(image, kernel, mode='valid')
        nmonsters = (conv == conv.max()).sum()

        return image.sum() - nmonsters * kernel.sum()



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
