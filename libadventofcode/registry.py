class NoSuchSolver(Exception):
    pass
class SolverAlreadyExists(Exception):
    pass



class SolversRegistry:
    def __init__(self):
        self._solvers = {}

    def register(self, challid, solver):
        if challid in self._solvers:
            raise SolverAlreadyExists("Multiple solvers for challenge id %s" % challid)

        self._solvers[challid] = solver

    def solver(self, challid):
        if challid not in self._solvers:
            raise NoSuchSolver("No solver for challenge %s" % challid)

        return self._solvers[challid]

    def solvers(self):
        return list(self._solvers)



global_registry = SolversRegistry()

def register(challid, solver):
    global_registry.register(challid, solver)

def solver(challid):
    return global_registry.solver(challid)

def solvers():
    return global_registry.solvers()
