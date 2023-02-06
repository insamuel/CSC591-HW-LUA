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
            row = t if type(t) == Row else Row(t)
            self.rows.append(row)
            for todo in [self.cols.x, self.cols.y]:
                for col in todo:
                    col.add(row.cells[col.col_position])

    def clone(self, init, x):
        data = Data({self.cols.names})
        map(init or {}, data.add(x))
        return data

    # Rounding numbers to 'places' (default=2)
    # For showCols, default = self.cols.y
    # No defaults for fun
    def stats(self, what, cols, nplaces):
        return dict(sorted({col.txt: col.rnd(getattr(col, what)(), nplaces) for col in cols or self.cols.y}.items()))