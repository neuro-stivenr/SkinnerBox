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