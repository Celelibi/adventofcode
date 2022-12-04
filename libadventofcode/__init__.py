import logging
import os
import re
import requests
import time

from . import registry
from . import solutions



input_cache_dir = ".inputs"



class TryAgain(Exception):
    def __init__(self, t):
        self.time = t



class AdventOfCode:
    def __init__(self, session, year=None):
        self._year = year
        if self._year is None:
            self._year = time.strftime("%Y")

        self._sess = requests.Session()
        self._sess.cookies["session"] = session



    def list(self):
        return registry.solvers()



    def download(self, chall):
        logging.info("Downloading data for challenge %s", chall)
        res = self._sess.get("https://adventofcode.com/%s/day/%s/input" % (self._year, chall))
        res.raise_for_status()
        return res.text



    def get_input(self, chall):
        fullpath = os.path.join(os.getcwd(), input_cache_dir)
        logging.debug("Checking if input cache directory exists at: %s", fullpath)
        if not os.path.exists(input_cache_dir):
            logging.info("Input cache directory doesn't exist, creating it")
            os.mkdir(input_cache_dir)

        cache_file = os.path.join(input_cache_dir, "input_%02d.txt" % int(chall))
        logging.debug("Checking for the existence of cached input file: %s", cache_file)
        if os.path.exists(cache_file):
            logging.info("Reading input from file: %s", cache_file)
            with open(cache_file) as fp:
                return fp.read()

        data = self.download(chall)
        logging.info("Saving input data to cache file: %s", cache_file)
        with open(cache_file, "w") as fp:
            fp.write(data)

        return data



    def submit_once(self, chall, solution, level):
        url = "https://adventofcode.com/%s/day/%s/answer" % (self._year, chall)
        data = {"level": level, "answer": solution}

        logging.info("Submitting solution %s to challenge %s, level %d", solution, chall, level)
        res = self._sess.post(url, data=data)
        res.raise_for_status()

        if "Did you already complete it?" in res.text:
            logging.info("Challenge %s, level %d already done.", chall, level)
            return

        if "That's the right answer!" in res.text:
            logging.info("Challenge %s, level %d solved!", chall, level)
            return

        if "That's not the right answer" in res.text:
            logging.info("Wrong solution to challenge %s, level %d.", chall, level)
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
        solver = registry.solver(day)

        data = self.get_input(day)

        logging.info("Solving challenge %s level 1", day)
        solution1 = solver.solve1(data)

        logging.info("Solving challenge %s level 2", day)
        solution2 = solver.solve2(data)

        if solution1 is not None:
            self.submit(day, solution1, 1)
        if solution2 is not None:
            self.submit(day, solution2, 2)



    def solve_all(self):
        challs = self.list()
        data = {}
        for n in challs:
            data[n] = self.get_input(n)

        solutions1 = {}
        for n in challs:
            logging.info("Solving challenge %s", n)
            solutions1[n] = registry.solver(n).solve1(data[n])

        solutions2 = {}
        for n in challs:
            logging.info("Solving challenge %s", n)
            solutions2[n] = registry.solver(n).solve2(data[n])

        for n in challs:
            if solutions1[n] is not None:
                self.submit(n, solutions1[n], 1)

        for n in challs:
            if solutions2[n] is not None:
                self.submit(n, solutions2[n], 2)
