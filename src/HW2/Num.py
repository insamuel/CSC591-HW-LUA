import math
import Utils


# Num summarizes a stream of numbers
class Num:
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.num_items = 0  # items seen
        self.mu = 0
        self.m2 = 0
        self.lo = math.inf  # lowest seen
        self.hi = -math.inf  # highest seen
        self.is_sorted = True  # no updates since last sort of data
        self.w = 1 if txt and txt[-1] == '+' else -1  # maximize or minimize column

    # Reservoir sampler
    def add(self, n: float):
        if n != '?':
            self.num_items += 1
            d = n - self.mu
            self.mu += (d/self.num_items)
            self.m2 += d*(n - self.mu)
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)


    # Central tendency; for Nums, this is mean
    def mid(self):
        return self.mu

    # Diversity; for Nums, this is standard deviation using Welford's alg
    def div(self):
        return 0 if (self.m2 < 0 or self.num_items < 2) else math.pow((self.m2 / (self.num_items - 1)), 0.5)

    # Rounding: Round the num to n places
    def rnd(self, x, n):
        return Utils.rnd(x, n)