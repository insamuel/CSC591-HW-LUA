import re
from Sym import Sym
from Num import Num


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
    def __init__(self, names):
        self.names = names  # All column names
        self.all = []       # All columns including the skipped ones
        self.klass = None   # The single dependent klass column (if it exists)
        self.x = []         # Independent columns
        self.y = []         # Dependent columns

        for c, s in enumerate(names):
            # Generate Nums and Syms from col names
            if re.match('^[A-Z]+', s):
                col = Num(c, s)             # Numerics start with uppercase
            else:
                col = Sym(c, s)
            self.all.append(col)

            if not re.findall("X$", s):     # Some columns are skipped
                if s[-1] in ['+', '-']:
                    self.y.append(col)
                else:
                    self.x.append(col)
                if s[-1] == '!':
                    self.klass = col

    ##
    # The add method updates the dependent and independent columns with
    # details from a given row. It does this by iterating over the x and y
    # lists and calling the add method for each column, passing in the
    # relevant cell from the row.cells list.
    ##
    def add(self, row):
        for _, names in enumerate([self.x, self.y]):
            for _, col in enumerate(names):
                col.add(row.cells[col.at])


