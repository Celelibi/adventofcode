import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    pieces = """....
....
....
####

....
.#..
###.
.#..

....
..#.
..#.
###.

#...
#...
#...
#...

....
....
##..
##..
"""
    pieces = np.array([[list(line) for line in p.splitlines()] for p in pieces.split("\n\n")])
    pieces = (pieces == "#")[:, ::-1]
    pieces_heights = np.count_nonzero(pieces.sum(axis=2), axis=1)

    @staticmethod
    def tetris(maxsim, shifts):
        shifts = (np.array(list(shifts)) == ">") * 2 - 1
        pg = np.zeros((maxsim * 4 + 4, 12), dtype=bool)
        pg[0, :] = True
        pg[:, [0, 8]] = True

        height = 0
        heights = [0]
        shift_idx = 0

        for i in range(maxsim):
            piece = Solver.pieces[i % Solver.pieces.shape[0]]
            y, x = height + 3 + 1, 3

            while True:
                shift = shifts[shift_idx]
                shift_idx = (shift_idx + 1) % shifts.shape[0]

                x += shift
                if np.any(pg[y:y+4, x:x+4] & piece):
                    x -= shift

                y -= 1
                if np.any(pg[y:y+4, x:x+4] & piece):
                    y += 1
                    break

            pg[y:y+4, x:x+4] |= piece
            height = max(height, y + Solver.pieces_heights[i % Solver.pieces.shape[0]] - 1)
            heights.append(height)

        return heights


    def solve1(self, data):
        return self.tetris(2022, data.strip())[-1]



    def solve2(self, data):
        N = 1000000000000
        heights = self.tetris(5000, data.strip())

        diffs = np.diff(heights)
        period = np.correlate(diffs[1:], diffs[:1000]).argmax() + 1
        assert np.all(diffs[2*period:] == diffs[period:-period])

        growth_per_period = heights[2*period] - heights[period]
        # Remove the first period (not repeating) with the "- 1"
        # Add it back with "period +" at the end
        return (N // period - 1) * growth_per_period + heights[period + N % period]



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
