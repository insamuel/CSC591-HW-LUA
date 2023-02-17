from Num import Num
from Sym import Sym

import Row

import re
from enum import Enum


# Holds summaries of columns
class Cols:
    ##
    # A NUM or SYM is generated based on whether s starts with an uppercase
    # letter or not.
    #
    # The generated NUM or SYM is appended to the all attribute.
    #
    # If s does not end with the character 'X', it is either appended to
    # the y or x attribute based on whether it ends with [!+-] or not. If
    # it ends with !, it sets the klass attribute to this NUM or SYM.
    #
    # names:    A list of all column names in the dataset.
    # all:      A list of all columns, including the skipped ones.
    # klass:    A single dependent class column (if it exists).
    # x:        A list of independent columns.
    # y:        A list of dependent columns.
    ##
    def __init__(n, s):

        if re.match('^[A-Z]', s) != None:
            col = Num(n, s)
        else:
            col = Sym(n, s)

        col.isIgnored   = bool(re.search('X$', col.txt))
        col.isKlass     = bool(re.search('!$', col.txt))
        col.isGoal      = bool(re.search('[!+-]$', col.txt))

        return col
