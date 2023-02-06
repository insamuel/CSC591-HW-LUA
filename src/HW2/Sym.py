# Sym's summarize a stream of symbols.
from collections import defaultdict
import math


class Sym:
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.num_items = 0  # items seen
        self.has = defaultdict(int)  # kept data

    # Add symbol value to Sym object
    def add(self, value):
        if value != "?":
            self.num_items += 1
            self.has[value] += 1

    # Calculates the mode, most common symbol
    def mid(self):
        mode = None
        most = -1
        for key in self.has:
            sym_count = self.has[key]
            if sym_count > most:
                most = sym_count
                mode = key
        return mode

    # Calculate diversity, which is entropy in the case of Sym
    def div(self, e=0):
        def fun(p):
            return p * math.log(p, 2)

        for n in self.has.values():
            e = e + fun(n / self.num_items)

        return -e

    # Rounding: For Sym just return value because can't round a sym
    def rnd(self, x, n):
        return x


