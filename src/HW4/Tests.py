import sys
import TestEngine
import Common
from Data import Data
from Num import Num
from Sym import Sym
from Row import Row
from Cols import Cols
from Utils import rnd, canPrint, rand, set_seed, read_csv

command_line_args = []



##
# Imports sys, TestEngine, Common, Num from Num, Sym from Sym, rnd,
# canPrint, rand, set_seed, csv from Utils
#
# Checks if it's possible to print the value of the "the" field in the
# "cfg" dictionary in the "Common" module.
#
# Call the "canPrint" function with the "Common.cfg['the']" argument and
# the string "Should be able to print the". If the "canPrint" function
# executes without raising an exception, the "eg_the" function returns
# True, which represents that the test passed.
##
@TestEngine.test
def eg_the():
    canPrint(Common.cfg['the'], 'Should be able to print the')
    return True

##
# Defines a test function named "eg_rand" using the @TestEngine.test
# decorator.
#
# Checks if two sets of random numbers generated with the same seed are
# equal, and if the midpoint of the set of random numbers is equal to 0.5.
#
# It creates two instances of the Num class, "num1" and "num2".
#
# It sets a seed for the random number generator using the set_seed
# function, with a value of 937162211. It uses a for loop to add 1000
# random numbers in the range of 0 to 1 to "num1".
#
# It sets the same seed for the random number generator again. It uses
# another for loop to add 1000 random numbers in the range of 0 to 1 to
# "num2".
#
# It calculates the midpoints of the "num1" and "num2" instances, rounded
# to 10 decimal places, and stores them in "m1" and "m2". It formats a
# string with "m1", "m2", and the rounded value of "m1". It calls the
# canPrint function to print the formatted string along with the message
# "M1 and M2 should be equal".
##
@TestEngine.test
def eg_rand():
    num1, num2 = Num(), Num()

    set_seed(937162211)
    for i in range(1, 10 ** 3 + 1):
        x = rand(0, 1)
        num1.add(x)

    set_seed(937162211)
    for i in range(1, 10 ** 3 + 1):
        num2.add(rand(0, 1))

    m1, m2 = round(num1.mid(), 10), round(num2.mid(), 10)
    results = "m1= {}, m2= {}, rounded= {}".format(m1, m2, round(m1, 1))
    canPrint(results, 'M1 and M2 should be equal')
    return m1 == m2 and .5 == round(m1, 1)

##
# Defines a test function named eg_sym using the @TestEngine.test
# decorator.
#
# Returns the result of the comparison between the calculated
# midpoint and 11/7 and the calculated variance and 0.787.
#
# The function creates an instance of the Sym class and adds
# some string values to it.
#
# The function then calculates the mode and entropy of the symbols and
# rounds the entropy value to 3 decimal places. It then prints the mode and
# entropy values in a formatted string.
#
# Returns true if the mode is "a" and the entropy value is 1.379.
##
@TestEngine.test
def eg_sym():
    s = Sym()

    test_vals = ["a", "a", "a", "a", "b", "b", "c"]

    for x in test_vals:
        s.add(x)

    # mode, entropy = s.mid(), rnd(s.div(), 3)
    # results = "mid= {}, div= {}".format(mode, entropy)
    # canPrint(results, 'Should be able to print mid and div')

    res = ('a' == s.mid()) and (1.379 == rnd(s.div(), 3))
    return res

##
# Defines a test function named eg_num using the @TestEngine.test
# decorator.
#
# Checks the Num class. It creates an instance of the Num class named n.
#
# It adds the elements of the list test_vals to the instance of Num using
# the add method.
#
# It calculates the midpoint (mean) and the variance of the elements added
# to the Num instance.
#
# It formats the midpoint, div values and the string "Should be
# able to print mid and div" into a single string and passes it to the
# function canPrint.
##
@TestEngine.test
def eg_num():
    n = Num()
    test_vals = [1,1,1,1,2,2,3]
    for x in test_vals:
        n.add(x)

    mid, div = n.mid(), round(n.div(), 3)
    results = "mid= {}, div= {}".format(mid, div)
    canPrint(results, 'Should be able to print mid and div')

    return 11/7 == mid and 0.787 == div

@TestEngine.test
def eg_csv():
    row_count = 0
    def line_handler(xs: Row):
        nonlocal row_count
        row_count += 1
    read_csv(Common.cfg["the"]["file"], line_handler)
    return row_count == 399

@TestEngine
def eg_duplicate_structure():
    d = Data(Common.cfg['the']['file'])
    

##
# Defines a function ALL using @TestEngine.test. This function calls other
# functions, whose names start with eg_, stored in Common.eg, one by one,
# and prints their results. The function also keeps track of the number of
# failed tests in the Common.fails variable. The function returns True at
# the end.
##
@TestEngine.test
def ALL():
    for k in Common.eg:
        if k != "ALL":
            print("\n−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−")
            if not TestEngine.runs(k):
                Common.fails += 1
    return True

##
# Checks if the script is being run as the main program and if so, it calls
# the TestEngine.runs function with the value of the eg key of the
# dictionary of Common.cfg as its argument. After the call to TestEngine
# runs, the program exits with the value of Common.fails as the exit status
# code.
##
if __name__ == "__main__":
    TestEngine.runs(Common.cfg["the"]["eg"])
    sys.exit(Common.fails)