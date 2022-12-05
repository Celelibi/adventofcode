import re

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        reqfields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
        r = re.compile(r'(...):')

        docs = data.split("\n\n")
        res = 0
        for doc in docs:
            fields = set(m.group(1) for m in r.finditer(doc))
            missingfields = reqfields - fields
            if len(missingfields) == 0:
                res += 1

        return res



    def solve2(self, data):
        reqfields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
        r = re.compile(r'(...):(\S*)')

        rules = {
            "byr": lambda x: int(x) in range(1920, 2003),
            "iyr": lambda x: int(x) in range(2010, 2021),
            "eyr": lambda x: int(x) in range(2020, 2031),
            "hgt": lambda x: (x[-2:] == "cm" and int(x[:-2]) in range(150, 194)) or (x[-2:] == "in" and int(x[:-2]) in range(50, 77)),
            "hcl": lambda x: re.fullmatch(r'#[0-9a-f]{6}', x) is not None,
            "ecl": lambda x: x in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
            "pid": lambda x: re.fullmatch(r'\d{9}', x) is not None,
            "cid": lambda x: True,
        }

        docs = data.split("\n\n")
        res = 0
        for doc in docs:
            passp = dict(m.groups() for m in r.finditer(doc))
            missingfields = reqfields - set(passp)
            if len(missingfields) == 0 and all(rules[k](v) for k, v in passp.items()):
                res += 1

        return res



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
