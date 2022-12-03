import abc



class Solver(object, metaclass=abc.ABCMeta):
    def __init__(self):
        self.solution = None

    @abc.abstractmethod
    def solve1(self, data):
        raise NotImplementedError("Method solve1 not implemented")

    @abc.abstractmethod
    def solve2(self, data):
        raise NotImplementedError("Method solve2 not implemented")
