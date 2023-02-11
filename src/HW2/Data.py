import numbers
import yaml
import math
import Common
import copy
import functools

from typing import List
from Cols import Cols
from Row import Row
from Utils import read_csv

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
        elif src_type == list: # else we were passed the columns as a string
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
