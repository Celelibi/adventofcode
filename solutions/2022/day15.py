import re

import numpy as np

from libadventofcode import base
from libadventofcode import registry
from libadventofcode.utils import Timer



class Solver(base.Solver):
    def solve1(self, data):
        data = np.array([re.findall(r"(-?\d+)", line) for line in data.splitlines()], dtype=int)
        sensors, beacons = data[:, :2], data[:, 2:]
        dist = np.abs(beacons - sensors).sum(axis=1)

        query = 2000000
        rem = dist - np.abs(sensors[:, 1] - query)
        valid_sensors = (rem > 0)
        ranges_from = sensors[valid_sensors, 0] - rem[valid_sensors]
        ranges_to = sensors[valid_sensors, 0] + rem[valid_sensors] + 1
        ranges = np.c_[ranges_from, ranges_to]
        ranges = ranges[ranges[:, 0].argsort()]

        cummax = np.maximum.accumulate(ranges[:, 1], axis=0)
        np.maximum(ranges[1:, 0], cummax[:-1], out=ranges[1:, 0])
        np.maximum(ranges[:, 0], ranges[:, 1], out=ranges[:, 1])

        beacons_onrow = np.unique(beacons[beacons[:, 1] == query, 0])
        bcn_cnt = (ranges[:, 0:1] <= beacons_onrow) & (beacons_onrow < ranges[:, 1:2])

        return (ranges[:, 1] - ranges[:, 0]).sum() - bcn_cnt.sum()



    def solve2(self, data):
        data = np.array([re.findall(r"(-?\d+)", line) for line in data.splitlines()], dtype=int)
        sensors, beacons = data[:, :2], data[:, 2:]
        dist = np.abs(beacons - sensors).sum(axis=1)

        bound = 4000000

        # rem[y, s] is the remaining distance from sensor s once row y is reached
        # Can be negative if row y is out of reach of sensor s
        with Timer("rem"):
            yrange = np.arange(bound + 1).reshape(-1, 1)
            rem = dist - np.abs(sensors[:, 1] - yrange)

        # range_from[y, s]..range_to[y, s] is the range of x values reached by sensor s on row y
        with Timer("ranges"):
            ranges_from = sensors[:, 0] - rem
            ranges_to = sensors[:, 0] + rem + 1
            np.clip(ranges_from, 0, bound, out=ranges_from)
            np.clip(ranges_to, 0, bound, out=ranges_to)

        # Sort those ranges by increasing begining values
        with Timer("sort"):
            with Timer("sort only"):
                idx = np.argsort(ranges_from, axis=1)
            with Timer("take_along_axis from"):
                ranges_from = np.take_along_axis(ranges_from, idx, axis=1)
            with Timer("take_along_axis to"):
                ranges_to = np.take_along_axis(ranges_to, idx, axis=1)

        with Timer("all_ranges"):
            all_ranges = np.stack((ranges_from, ranges_to), axis=-1)
            ranges_from = ranges_to = None

        # Move the begining of ranges such that it never overlaps with a previous range
        with Timer("cummax"):
            cummax_to = np.maximum.accumulate(all_ranges[:, :, 1], axis=1)
            np.maximum(all_ranges[:, 1:, 0], cummax_to[:, :-1], out=all_ranges[:, 1:, 0])
            cummax_to = None

        # Normalize range ends so that intervals never cross
        with Timer("Normalize ends"):
            np.maximum(all_ranges[:, :, 0], all_ranges[:, :, 1], out=all_ranges[:, :, 1])

        with Timer("Gap after"):
            gap = (all_ranges[:, :-1, 1] < all_ranges[:, 1:, 0])

        y, i = np.argwhere(gap)[0]
        return np.dot([all_ranges[y, i, 1], y], [bound, 1])



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
