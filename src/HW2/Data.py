import numbers
import yaml
from pathlib import Path
from Cols import Cols
from Row import Row
from Utils import csv, rnd

my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'config.yml'

with config_path.open() as config_file:
    cfg = yaml.safe_load(config_file)


# Holds rows and their summaries in Cols.
class Data:
    def __init__(self, src):
        self.cols = None  # Summaries of data
        self.rows = []  # Kept data

        if type(src) == str:
            csv(src, self.add)  # If string name do IO on csv file and send pass the add row func
        else:
            for _, row in src:  # Else given rows so no processing just add
                self.add(row)

    def add(self, t: Row):

        if not self.cols:
            self.cols = Cols(t)
        else:
            t = t.cells if hasattr(t, "cells") else Row(t)
            self.rows.append(t)
            self.cols.add(t)

    def clone(self, init, x):
        data = Data({self.cols.names})
        map(init or {}, data.add(x))
        return data

    # Rounding numbers to 'nplaces' (default=2)
    # For cols, default = self.cols.y
    # No defaults for what
    def stats(self, what, cols, nplaces):
        if not cols:
            cols = self.cols.y
        t = {}
        for col in cols:
            v = what(col)
            if isinstance(v, numbers.Number):
                t[col.txt] = rnd(v, nplaces)
            else:
                t[col.txt] = v
        return t