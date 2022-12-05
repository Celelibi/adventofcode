from libadventofcode import base
from libadventofcode import registry



def execasm(prog):
    executed = [0] * len(prog)
    pc = 0
    acc = 0

    while not executed[pc]:
        executed[pc] = True
        inst, val = prog[pc]
        if inst == "nop":
            pc += 1
        elif inst == "acc":
            acc += val
            pc += 1
        elif inst == "jmp":
            pc += val
        else:
            raise RuntimeError("Invalid instruction: " + inst)

        if pc == len(prog):
            break

        if pc not in range(len(prog)):
            raise RuntimeError("Segmentation Fault at 0x%04x" % pc)

    return pc, acc


class Solver(base.Solver):
    def solve1(self, data):
        data = data.splitlines()
        prog = [(l[:3], int(l[4:])) for l in data]
        return execasm(prog)[1]



    def solve2(self, data):
        data = data.splitlines()
        prog = [(l[:3], int(l[4:])) for l in data]
        for i, (inst, val) in enumerate(prog):
            newprog = prog.copy()
            if inst == "nop":
                newprog[i] = ("jmp", val)
            elif inst == "jmp":
                newprog[i] = ("nop", val)

            pc, acc = execasm(newprog)
            if pc == len(prog):
                return acc



registry.register((__name__.split(".")[-2], str(int(__name__[-2:]))), Solver())
