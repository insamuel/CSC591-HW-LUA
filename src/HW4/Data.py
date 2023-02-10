import math
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
        self.cols = None        # Summaries of data
        self.rows = []          # Kept data

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
    # arguments: self, row1, and row2.
    #
    # Initialized several variables: s1 and s2 to 0, ys to self.cols
    # y, x and y to undefined.
    ##
    def better(self, row1, row2):
        s1  = 0
        s2  = 0
        ys  = self.cols.y
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
            x = col.norm(row1.cells[col.col_position])
            y = col.norm(row2.cells[col.col_position])
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
    def dist(self, row1, row2, cols, n = 0, d = 0):
        if cols is None:
            cols = self.cols.x

        for col in cols:
            n += 1
            d += pow(col.dist(row1.cells[col.col_position], row2.cells[col.col_position]), self.p)

        return pow(d / n, 1 / self.p)

    ##
    # Sorts a list of rows based on their distance to a reference row, row1.
    # Sorting is performed in ascending order of the distance, so the
    # closest row will come first in the sorted list. The function takes
    # four arguments: self, row1, rows, and cols.
    #
    # If the rows argument is None, the function sets rows to self.rows.
    #
    # Maps the rows list to a list of dictionaries. Each dictionary
    # contains the row and its dist to the row1. The dist is calculated
    # using the self.dist method and passing it row1, row2, and cols as
    # arguments. Then, it sorts the list of dictionaries based on
    # the dist key and returns the sorted list.
    ##
    def around(self, row1, rows, cols):
        return sorted(list(map(rows or self.rows, lambda row2: {"row": row2, "dist": self.dist(row1, row2, cols)})), key = lambda x: x["dist"])

    ##
    # Returns a tuple of two lists (left and right), two values (A and B)
    # mid row, mid and a number c.
    #
    # Sets the value of rows to self.rows if rows is not provided.
    # Calculates a sample of rows using the many function, and sets A to
    # the first element of the sample or the value of above if provided. B
    # is set to the row from self.around(A, some) that has the largest
    # distance from A.
    #
    # Calculates the value of c as the distance between A and B, and
    # initializes the lists left and right as empty.
    #
    # Sorts the rows by the result of the project function applied to each
    # row and maps it to a list of dictionaries containing the row and its
    # corresponding distance from A and B. The function then iterates over
    # this sorted list, adds each row to either left or right based on its
    # index, and sets mid to the row in the middle.
    ##
    # def half(self, rows, cols, above):
    #     def project(row):
    #         return {"row": row, "dist": math.cos(dist(row, A), dist(row, B), c)}
    #
    #     def dist(row1, row2):
    #         return self.dist(row1, row2, cols)
    #
    #     if rows is None:
    #         rows = self.rows
    #
    #     some = many(rows, self.Sample)
    #
    #     return left, right, A, B, mid, c
    #

    def furthest(self, row1):
        t = self.around(row1, self.rows, self.cols)
        return t[len(t)]

