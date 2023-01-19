import math


# Num summarizes a stream of numbers
class Num:
    def __init__(self, col_position=0, col_name=""):
        self.num_items = 0  # items seen
        self.mu = 0
        self.m2 = 0
        self.lo = math.inf  # lowest seen
        self.hi = -math.inf  # highest seen
        self.is_sorted = True  # no updates since last sort of data

    # Reservoir sampler
    def add(self, n):
        if n != '?':
            value = int(n)
            self.num_items += 1
            d = value - self.mu
            self.mu += d/self.num_items
            self.m2 += d*(self.num_items - self.mu)
            self.lo = min(self.lo, value)
            self.hi = max(self.hi, value)


    # Central tendency; for Nums, this is mean
    def mid(self):
        return self.mu

    # Diversity; for Nums, this is standard deviation using Welford's alg
    def div(self):
        if self.m2 < 0 or self.num_items < 2:
            return 0
        else:
            return math.pow(self.m2/(self.num_items-1), 0.5)
