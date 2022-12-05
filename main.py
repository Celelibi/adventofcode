#!/usr/bin/env python3

import argparse
import locale
import logging
import logging.config
import os
import sys

import libadventofcode
import solutions # pylint: disable=unused-import



SELFPATH = os.path.dirname(os.path.realpath(sys.argv[0]))



def main():
    locale.setlocale(locale.LC_ALL, '')
    logging.config.fileConfig(os.path.join(SELFPATH, "logconf.ini"))

    parser = argparse.ArgumentParser(description="Bot de validation AdventOfCode")
    parser.add_argument("session", metavar="COOKIE", help="Cookie de session à utiliser")
    parser.add_argument("--list", "-l", action="store_true", help="List solvable challenges")
    parser.add_argument("--all", "-a", action="store_true", help="Solve all challenges")
    parser.add_argument("--day", "-d", help="Solve the given day challenge")
    parser.add_argument("--year", "-y", help="Solve the challenges of a given year (default, now)")
    parser.add_argument("--verbose", "-v", action="count", help="Augmente le niveau de verbosité")

    args = parser.parse_args()

    session = args.session
    listchall = args.list
    solveall = args.all
    solveday = args.day
    solveyear = args.year
    verbose = args.verbose

    if verbose is not None:
        loglevels = ["WARNING", "INFO", "DEBUG", "NOTSET"]
        verbose = min(len(loglevels), verbose) - 1
        logging.getLogger().setLevel(loglevels[verbose])
        logging.debug("Log level set to %s", loglevels[verbose])

    if solveall and solveday is not None:
        print("--all and --day are mutually exclusive")
        return

    aoc = libadventofcode.AdventOfCode(session, solveyear)

    if listchall:
        print("Known challenge solvers:")
        for c in aoc.list():
            print("%s/%s" % c)

    if solveall:
        aoc.solve_all()

    if solveday is not None:
        aoc.solve_day(solveday)



if __name__ == '__main__':
    main()
