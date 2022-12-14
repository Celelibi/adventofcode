import logging
import os
import re
import sys
import time

import requests

from . import registry



input_cache_dir_base = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), ".inputs")



class TryAgain(Exception):
    def __init__(self, t):
        self.time = t



class Timer:
    def __init__(self, prefix="time", fmt="%f seconds", logger="Timer", loglevel=logging.DEBUG, autoprint=True):
        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        if prefix is None:
            self._fmt = fmt
        else:
            self._fmt = prefix + ": " + fmt

        self._logger = logger
        self._loglevel = loglevel
        self._autoprint = autoprint

        self._elapsed = 0
        self._stattime = None
        self.start()

    def start(self):
        self._stattime = time.perf_counter()

    def stop(self):
        self._elapsed = time.perf_counter() - self._stattime
        if self._autoprint:
            self.print()

    def print(self):
        self._logger.log(self._loglevel, self._fmt, self._elapsed)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()



class AdventOfCode:
    def __init__(self, session, year=None):
        self._year = year
        if self._year is None:
            self._year = time.strftime("%Y")

        self._input_cache_dir = os.path.join(input_cache_dir_base, self._year)
        self._sess = requests.Session()
        self._sess.cookies["session"] = session



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
        return solutions[level - 1]



    def submit_once(self, chall, solution, level):
        solution = str(solution)
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
        while True:
            try:
                self.submit_once(chall, solution, level)
            except TryAgain as e:
                logging.info("Sleeping for %d seconds", e.time)
                time.sleep(e.time)
            else:
                break



    def solve_day(self, day):
        solver = registry.solver((self._year, day))

        data = self.get_input(day)

        logging.info("Solving challenge %s level 1", day)
        with Timer():
            solution1 = solver.solve1(data)

        logging.info("Solving challenge %s level 2", day)
        with Timer():
            solution2 = solver.solve2(data)

        if solution1 is not None:
            self.submit(day, solution1, 1)
        if solution2 is not None:
            self.submit(day, solution2, 2)



    def solve_all(self):
        challs = self.list(True)
        data = {}
        for n in challs:
            data[n] = self.get_input(n[1])

        solutions1 = {}
        for n in challs:
            logging.info("Solving challenge %s level 1", n)
            with Timer():
                solutions1[n] = registry.solver(n).solve1(data[n])

        solutions2 = {}
        for n in challs:
            logging.info("Solving challenge %s level 2", n)
            with Timer():
                solutions2[n] = registry.solver(n).solve2(data[n])

        for n in challs:
            if solutions1[n] is not None:
                self.submit(n[1], solutions1[n], 1)

        for n in challs:
            if solutions2[n] is not None:
                self.submit(n[1], solutions2[n], 2)
