import numbers
import yaml
import math
import Common
import copy

from typing import List
from Cols import Cols
from Row import Row
from Utils import read_csv, rnd, get_rand_items, cos

with open("config.yml", 'r') as config_file:
    cfg = yaml.safe_load(config_file)


# Holds rows and their summaries in Cols.
class Data:
    def __init__(self, src):
        self.rows = []
        self.cols =  None
        self.src = src

        ## if the src is string then
        ## it reads the file and then calls the add method to add each row
        src_type = type(src)
        if src_type == str :
            read_csv(src, self.add)
        elif src_type == List[str]: # else we were passed the columns as a string
            self.add(src)
        else:
            raise Exception("Unsupported type in Data constructor")

    def add(self, xs: list[str]):

        if not self.cols:
            self.cols = Cols(xs)
        else:
            new_row = Row(xs)
            self.rows.append(new_row)
            self.cols.add(new_row)

    # Rounding numbers to 'places' (default=2)
    # For showCols, default = self.cols.y
    # No defaults for fun
    # def stats(self, places, showCols, fun):
    #     if not showCols:
    #         showCols = self.cols.y
    #     t = {}
    #     for col in showCols:
    #         v = fun(col)
    #         if isinstance(v, numbers.Number):
    #             t[col.col_name] = rnd(v, places)
    #         else:
    #             t[col.col_name] = v
    #     return t

    def clone(self):
        cloned_data = copy.deepcopy(self)
        return cloned_data
        

    ##
    # Defines a function "better" determines if row1 dominates row2 based
    # on a comparison method called "Zitzler04". The function takes three
    # arguments: i, row1, and row2.
    #
    # Initialized several variables: s1 and s2 to 0, ys to i.cols
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
    def dist(self, row1: Row, row2: Row, cols: Cols, n = 0, d = 0):
        if cols is None:
            cols = self.cols.x

        p =  Common.cfg['the']['p']
        for col in cols:
            n += 1
            d += pow(col.dist(row1.cells[col.at], row2.cells[col.at]), p)

        return pow(d / n, 1 /  p)

    def around(self, rowA: Row, rows):
        selected_rows = rows if rows != None else self.rows
        def compare(rowB: Row, rowC: Row):
            distAB = self.dist(rowA, rowB)
            distAC = self.dist(rowA, rowC)
            if(distAB < distAC):
                return -1
            elif(distAB > distAC):
                return 1
            return 0
        selected_rows.sort(key=compare)
        return selected_rows

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
    # def around(self, row1, rows, cols):
    #     return sorted(list(map(rows or self.rows, lambda row2: {"row": row2, "dist": self.dist(row1, row2, cols)})), key = lambda x: x["dist"])

    
    
    
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
    def half(self, cols: Cols, above: Row, rows):
        selected_rows = rows if rows != None else self.rows
        sample = Common.cfg['the']['sample']
        some = get_rand_items(selected_rows, sample)

        A = above if above != None else some[0] # Row A

        far = Common.cfg['the']['far']
        B_i = math.floor(far * len(rows))
        B = self.around(A, some)[B_i] # Row B

        c = self.dist(A, B)
        
        def distance(row1: Row, row2: Row):
            return self.dist(row1, row2, cols)
        def project(row: Row):
            return cos(self.dist(row, A), self.dist(row, B), c) #returns x,y values

        projections = []
        for item in rows:
            proj_result = project(item)
            projections.append({'row': item, 'projection': proj_result})

        def projection_sorter(projA, projB):
            return projA.x - projB.x
            
        projections.sort(key=projection_sorter)

        left = []
        right = []
        mid = {}
        for i, item in projections:
            if i < math.floor(len(rows) / 2):
                left.append(item.row)
                mid = item.row
            else:
                right.append(item.row)

        return {
                'left': left,
                'right': right,
                'A': A,
                'B': B,
                'mid': mid,
                'c': c
                }

    
    def cluster(self, rows, min, cols, above: Row):
        selected_rows = rows if rows != None else self.rows
        selected_min = min if min != None else math.pow(len(rows), Common.cfg['the']['min'])
        selected_cols = cols if cols != None else self.cols.x
        
        if len(selected_rows) > (2 * selected_min):
            node = self.half(selected_cols, above, selected_rows)
            node.left = self.cluster(node.left, min, selected_cols, node.A)
            node.right = self.cluster(node.right, min, selected_cols, node.B)
        
        node['data'] = copy.deepcopy(selected_rows)
        return node

    def sway(self, rows, min, cols, above):
        selected_rows = rows if rows != None else self.rows
        selected_min = min if min != None else math.pow(len(rows), Common.cfg['the']['min'])
        selected_cols = cols if cols != None else self.cols.x

        if len(selected_rows) > (2 * selected_min):
            node = self.half(selected_cols, above, selected_rows)
            node_copy = copy.deepcopy(node)
            if self.better(node.B, node.A): 
                node_copy.left = node.right
                node_copy.right = node.left
                node_copy.A = node.B
                node_copy.B = node.A
                node_copy.left = self.sway(node_copy.left, selected_min, selected_cols, node_copy.A)
        node_copy['data'] = copy.deepcopy(selected_rows)
        return node_copy
            
                
        