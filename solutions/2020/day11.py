import numpy as np
import scipy.signal as spsig

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        data = np.array([list(l) for l in data.splitlines()])
        mapseats = (data == "L")

        mask = np.ones((3, 3), dtype=np.int)
        mask[1, 1] = 0

        mapoccupied = np.zeros_like(mapseats, dtype=np.int)

        while True:
            occneigh = spsig.convolve2d(mapoccupied, mask, mode="same")
            newmapoccupied = mapoccupied.copy()
            newmapoccupied |= ((occneigh == 0) & mapseats)
            newmapoccupied &= ~(occneigh >= 4)
            if np.all(mapoccupied == newmapoccupied):
                break
            mapoccupied = newmapoccupied.astype(np.int)

        return np.sum(mapoccupied)



    def solve2(self, data):
        data = np.array([list(l) for l in data.splitlines()])
        mapseats = (data == "L")

        # Define a different mask for each cell
        masks = np.zeros(mapseats.shape + mapseats.shape, dtype=np.int)

        # Build the list of coordinates of the seats ordered by rows
        coordseats = np.argwhere(mapseats)
        coordseats = coordseats[np.lexsort((coordseats[:, 1], coordseats[:, 0]))]
        # Make pairs of coord of seats next to each other
        coord = np.hstack((coordseats[:-1], coordseats[1:]))
        coord = coord[coord[:, 0] == coord[:, 2]]
        masks[tuple(coord.T)] = 1
        masks[tuple(coord[:, [2, 3, 0, 1]].T)] = 1

        # Same vertically
        coordseats = coordseats[np.lexsort((coordseats[:, 0], coordseats[:, 1]))]
        coord = np.hstack((coordseats[:-1], coordseats[1:]))
        coord = coord[coord[:, 1] == coord[:, 3]]
        masks[tuple(coord.T)] = 1
        masks[tuple(coord[:, [2, 3, 0, 1]].T)] = 1

        #Same for the diagonal
        coordseats = coordseats[np.lexsort((coordseats[:, 0], coordseats[:, 0] - coordseats[:, 1]))]
        coord = np.hstack((coordseats[:-1], coordseats[1:]))
        coord = coord[coord[:, 0] - coord[:, 1] == coord[:, 2] - coord[:, 3]]
        masks[tuple(coord.T)] = 1
        masks[tuple(coord[:, [2, 3, 0, 1]].T)] = 1

        #Same for the anti-diagonal
        coordseats = coordseats[np.lexsort((coordseats[:, 0], coordseats[:, 0] + coordseats[:, 1]))]
        coord = np.hstack((coordseats[:-1], coordseats[1:]))
        coord = coord[coord[:, 0] + coord[:, 1] == coord[:, 2] + coord[:, 3]]
        masks[tuple(coord.T)] = 1
        masks[tuple(coord[:, [2, 3, 0, 1]].T)] = 1

        mapoccupied = np.zeros_like(mapseats, dtype=np.int)

        while True:
            occneigh = (masks * mapoccupied).sum(axis=(2, 3))
            newmapoccupied = mapoccupied.copy()
            newmapoccupied |= ((occneigh == 0) & mapseats)
            newmapoccupied &= ~(occneigh >= 5)
            if np.all(mapoccupied == newmapoccupied):
                break
            mapoccupied = newmapoccupied.astype(np.int)

        return np.sum(mapoccupied)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
