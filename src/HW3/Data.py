import numbers

import yaml

from Cols import Cols
from Row import Row
from Utils import csv, rnd

with open("config.yml", 'r') as config_file:
    cfg = yaml.safe_load(config_file)


# Holds rows and their summaries in Cols.
class Data:
    def __init__(self, src):
        self.cols = None  # Summaries of data
        self.rows = []  # Kept data

        if src:
            csv(src, self.add)  # If string name do IO on csv file and send pass the add row func
        else:
            for _, row in src:  # Else given rows so no processing just add
                self.add(row)

    def add(self, xs: Row):

        if not self.cols:
            self.cols = Cols(xs)
        else:
            row = xs if type(xs) == Row else Row(xs)
            self.rows.append(row)
            for todo in [self.cols.x, self.cols.y]:
                for col in todo:
                    col.add(row.cells[col.col_position])

    # Rounding numbers to 'places' (default=2)
    # For showCols, default = self.cols.y
    # No defaults for fun
    def stats(self, places, showCols, fun):
        if not showCols:
            showCols = self.cols.y
        t = {}
        for col in showCols:
            v = fun(col)
            if isinstance(v, numbers.Number):
                t[col.col_name] = rnd(v, places)
            else:
                t[col.col_name] = v
        return t

    ##
    # Defines a function "better" determines if row1 dominates row2 based
    # on a comparison method called "Zitzler04". The function takes three
    # arguments: i, row1, and row2.
    #
    # Initialized several variables: s1 and s2 to 0, ys to i.cols
    # y, x and y to undefined.
    ##
    def better(i, row1, row2):
        s1  = 0
        s2  = 0
        ys  = i.cols.y
        x, y

        ##
        # Calculates the values of x and y by calling the norm method on
        # each element of ys and passing the corresponding cell value from
        # row1 and row2 respectively.
        #
        # s1 and s2 are then updated
        #
        # Returns true if row1 dominates row2 based on the comparison by
        # dividing s1 by the number of elements in ys and comparing it to
        # s2 by the number of elements in ys.
        ##
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))

        return s1/len(ys) < s2/len(ys)

    ##
    # Defines a function "dist" that calculates the distance between two
    # rows row1 and row2.
    #
    # col.dist calculates the distance between two values in a column.
    # row1.cells[col.at] and row2.cells[col.at] are the values in the
    # column col of row1 and row2 respectively.
    ##
    def dist(i, row1, row2, cols, n = 0, d = 0):
        if cols is None:
            cols = i.cols.x

        for col in cols:
            n += 1
            d += pow(col.dist(row1.cells[col.at], row2.cells[col.at]), the.p)

        return pow(d / n, 1 / the.p)