import numpy as np

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        dirs_offsets = {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}
        data = [line.split(" ") for line in data.splitlines()]
        data = [dirs_offsets[d] + [int(l)] for d, l in data]

        head = np.array([0, 0])
        tail = np.array([0, 0])
        prev_head = np.array([0, 0])
        seen = {(0, 0)}

        for dx, dy, l in data:
            for _ in range(l):
                head += [dx, dy]
                if np.max(np.abs(head - tail)) > 1:
                    tail = prev_head
                    seen.add(tuple(tail))

                prev_head = head.copy()

        return len(seen)



    def solve2(self, data):
        dirs_offsets = {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}
        data = [line.split(" ") for line in data.splitlines()]
        data = [dirs_offsets[d] + [int(l)] for d, l in data]

        string = np.zeros((10, 2), dtype=int)
        prev_string = string.copy()
        seen = {(0, 0)}

        for dx, dy, l in data:
            for step in range(l):
                string[0] += [dx, dy]

                for t in range(string.shape[0] - 1):
                    if np.max(np.abs(string[t] - string[t + 1])) > 1:
                        # If string[t] moved to far, let's fix string[t + 1]

                        if np.min(np.abs(string[t] - string[t + 1])) == 0:
                            # If the next link is in the same row or column, move that way
                            string[t + 1] += (string[t] - string[t + 1]) // 2

                        elif np.abs(string[t] - prev_string[t]).sum() == 1:
                            # If string[t] moved in a straight line, move where it was
                            string[t + 1] = prev_string[t]
                        else:
                            # If string[t] moved diagonally, follow the motion
                            string[t + 1] += string[t] - prev_string[t]

                seen.add(tuple(string[-1]))
                prev_string = string.copy()

        return len(seen)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
