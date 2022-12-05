import cypari2

from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        p = 20201227
        gen = 7
        pubkeys = [int(k) for k in data.splitlines()]
        gp = cypari2.Pari()
        privkeys = [gp.znlog(k, gp.Mod(gen, p)) for k in pubkeys]
        res = pow(gen, privkeys[0] * privkeys[1], p)
        return int(res)



    def solve2(self, data):
        return 0



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
