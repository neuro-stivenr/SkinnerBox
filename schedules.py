from numpy.random import binomial, shuffle
from typing import List

class FixedRatio:

    def __init__(self, ratio:int):
        self.ratio = ratio
        self.counter = 0

    def press(self):
        self.counter += 1
        if (self.counter % self.ratio) == 0:
            return True
        else:
            return False

class ProbRatio:

    def __init__(self, p:float):
        self.p = p
        self.counter = 0

    def press(self):
        self.counter += 1
        if bool(binomial(1, self.p)):
            return True
        else:
            return False

def ProbRatioBlock(ps:List[float]) -> List[ProbRatio]:
    shuffle(ps)
    return [ProbRatio(p) for p in ps]
