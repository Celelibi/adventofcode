import logging
import os
import re
import sys
import time

import requests

from . import registry
from .utils import Timer



input_cache_dir_base = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), ".inputs")



class TryAgain(Exception):
    def __init__(self, t):
        self.time = t

class NotSolvedError(Exception):
    pass


class AdventOfCode:
    def __init__(self, session, year=None, submit=True):
        self._year = year
        if self._year is None:
            self._year = time.strftime("%Y")

        self._input_cache_dir = os.path.join(input_cache_dir_base, self._year)
        self._sess = requests.Session()
        self._sess.cookies["session"] = session
        self._submit = submit



    def list(self, this_year_only=False):
        solvers = []
        for y, s in registry.solvers():
            if not this_year_only or self._year == y:
                solvers.append((y, s))

        return solvers



    def download(self, chall):
        logging.info("Downloading data for challenge %s", chall)
        res = self._sess.get("https://adventofcode.com/%s/day/%s/input" % (self._year, chall))
        res.raise_for_status()
        return res.text



    def get_input(self, chall):
        fullpath = os.path.join(os.getcwd(), self._input_cache_dir)
        logging.debug("Creating cache directory %s if necessary", fullpath)
        os.makedirs(self._input_cache_dir, exist_ok=True)

        cache_file = os.path.join(self._input_cache_dir, "input_%02d.txt" % int(chall))
        logging.debug("Checking for the existence of cached input file: %s", cache_file)
        if os.path.exists(cache_file):
            logging.info("Reading input from file: %s", cache_file)
            with open(cache_file, encoding="utf-8") as fp:
                return fp.read()

        data = self.download(chall)
        logging.info("Saving input data to cache file: %s", cache_file)
        with open(cache_file, "w", encoding="utf-8") as fp:
            fp.write(data)

        return data



    def get_already_done_solution(self, chall, level):
        url = "https://adventofcode.com/%s/day/%s" % (self._year, chall)

        logging.info("Retrieving solution of the validated challenge %s, level %d", chall, level)
        res = self._sess.get(url)
        res.raise_for_status()

        solutions = re.findall(r'Your puzzle answer was <code>([^<]*)</code>', res.text)
        if len(solutions) < level:
            raise NotSolvedError(f"Level {level} not solved yet")

        return solutions[level - 1]



    def submit_once(self, chall, solution, level):
        url = "https://adventofcode.com/%s/day/%s/answer" % (self._year, chall)
        data = {"level": level, "answer": solution}

        logging.info("Submitting solution %s to challenge %s, level %d", solution, chall, level)
        res = self._sess.post(url, data=data)
        res.raise_for_status()

        if "Did you already complete it?" in res.text:
            logging.info("Challenge %s, level %d already done.", chall, level)
            actual_solution = self.get_already_done_solution(chall, level)
            if solution == actual_solution:
                logging.info("%s is the correct solution", solution)
            else:
                logging.error("%s is incorrect, should be %s", solution, actual_solution)
            return

        if "That's the right answer!" in res.text:
            logging.info("Challenge %s, level %d solved!", chall, level)
            return

        if "That's not the right answer" in res.text:
            logging.error("Wrong solution to challenge %s, level %d.", chall, level)
            return

        if "You gave an answer too recently" in res.text:
            match = re.search(r'You have (?:(\d)m )?(\d+)s left to wait.', res.text)
            if match is None:
                print(res.text)
                raise ValueError("Unknown timing")

            t = int(match.group(2))
            if match.group(1):
                t += int(match.group(1)) * 60

            logging.info("Should wait %d seconds before retrying", t)
            raise TryAgain(t)

        print(res.text)



    def submit(self, chall, solution, level):
        solution = str(solution)

        if not self._submit:
            logging.info("Not sending solution %s for challenge %s.%d", solution, chall, level)
            try:
                actual_solution = self.get_already_done_solution(chall, level)
            except NotSolvedError:
                logging.debug("Challenge %s.%d wasn't solved", chall, level)
                return

            if solution == actual_solution:
                logging.info("%s is the correct", solution)
            else:
                logging.error("%s is wrong, should be %s", solution, actual_solution)

            return

        while True:
            try:
                self.submit_once(chall, solution, level)
            except TryAgain as e:
                logging.info("Sleeping for %d seconds", e.time)
                time.sleep(e.time)
            else:
                break



    def solve_day(self, day, data=None, level=None):
        if level not in (None, 1, 2):
            raise ValueError("level must be None, 1 or 2")

        solver = registry.solver((self._year, day))

        if data is None:
            data = self.get_input(day)

        solution1 = solution2 = None

        if level is None or level == 1:
            logging.info("Solving challenge %s level 1", day)
            with Timer():
                solution1 = solver.solve1(data)

        if level is None or level == 2:
            logging.info("Solving challenge %s level 2", day)
            with Timer():
                solution2 = solver.solve2(data)

        if solution1 is not None:
            self.submit(day, solution1, 1)
        if solution2 is not None:
            self.submit(day, solution2, 2)



    def solve_all(self, level=None):
        if level not in (None, 1, 2):
            raise ValueError("level must be None, 1 or 2")

        challs = self.list(True)
        data = {}
        for n in challs:
            data[n] = self.get_input(n[1])

        solutions1 = {}
        if level is None or level == 1:
            for n in challs:
                logging.info("Solving challenge %s/%s level 1", *n)
                with Timer():
                    solutions1[n] = registry.solver(n).solve1(data[n])

        solutions2 = {}
        if level is None or level == 2:
            for n in challs:
                logging.info("Solving challenge %s/%s level 2", *n)
                with Timer():
                    solutions2[n] = registry.solver(n).solve2(data[n])

        for n in challs:
            if n in solutions1 and solutions1[n] is not None:
                self.submit(n[1], solutions1[n], 1)

        for n in challs:
            if n in solutions2 and solutions2[n] is not None:
                self.submit(n[1], solutions2[n], 2)
