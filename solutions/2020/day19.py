from libadventofcode import base
from libadventofcode import registry



class Solver(base.Solver):
    def solve1(self, data):
        rules, data = data.split("\n\n")
        rules, data = rules.split("\n"), data.split("\n")

        prules = {}
        for r in rules:
            n, e = r.split(": ")
            if e.startswith('"'):
                prules[int(n)] = e[1:-1]
                continue
            e = [[int(v) for v in s.split()] for s in e.split(" | ")]
            prules[int(n)] = e

        rules = prules
        del prules

        def parse(s, r):
            def matchseq(s, seq):
                if seq == []:
                    yield s
                else:
                    g = parse(s, seq[0])
                    for t in g:
                        yield from matchseq(t, seq[1:])

            rule = rules[r]
            if isinstance(rule, str):
                if s.startswith(rule):
                    yield s[len(rule):]
            else:
                for seq in rule:
                    yield from matchseq(s, seq)

        return sum(any(t == "" for t in parse(l, 0)) for l in data)


    def solve2(self, data):
        data = data.replace("\n8: 42\n", "\n8: 42 | 42 8\n")
        data = data.replace("\n11: 42 31\n", "\n11: 42 31 | 42 11 31\n")
        return self.solve1(data)



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
