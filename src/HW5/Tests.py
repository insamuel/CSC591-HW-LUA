import sys
import TestEngine
import Common
import Repgrid

from Data import Data
from Num import Num
from Sym import Sym
from Row import Row
from Cols import Cols
from Utils import rnd, canPrint, rand, set_seed, read_csv, cliffs_delta

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
    num1 = Num()
    num2 = Num()

    for i in range(10000):
        num1.add(rand())
    for i in range(10000):
        num2.add(pow(rand(), 2))

    mid = num1.mid()
    mid2 = num2.mid()
    return rnd(num1.mid(), 1) == 0.5 and num1.mid() > num2.mid()

@TestEngine.test
def eg_csv():
    row_count = 0
    def line_handler(xs: Row):
        nonlocal row_count
        row_count += 1
    read_csv(Common.cfg["the"]["file"], line_handler)
    return row_count == 399

@TestEngine.test
def eg_duplicate_structure():
    d1 = Data(Common.cfg['the']['file'])
    d2 = d1.clone()
    return len(d1.rows) == len(d2.rows) and d1.cols.y[1].w == d2.cols.y[1].w and d1.cols.y[1].at == d2.cols.y[1].at


def show_cluster(cluster_res, cols, n_places, level):
    if cluster_res != None:
        report_string = ('|.. '*level)

        data = cluster_res['data']

        if 'left' not in cluster_res:
            report_string+=  str(data.rows[-1].cells[-1])
        else:
            print_val = rnd(100 * cluster_res['c'])
            report_string+=  str(rnd(100 * cluster_res['c']))
        print(report_string)

        show_cluster(cluster_res['left'] if 'left' in cluster_res else None, cols, n_places, level + 1)
        show_cluster(cluster_res['right'] if 'right' in cluster_res else None, cols, n_places, level + 1)

def show_tree(tree, level = None):
    if tree != None:
        level = level if level != None else 0
        report_string = ('|.. '*level)
        data = tree['data']
        report_string+= str(len(data.rows))

        if level == 0 or 'left' not in tree:
            report_string+= '   ' + str(data.stats())
            
        print(report_string)
        show_tree(tree['left'] if 'left' in tree else None, level + 1)
        show_tree(tree['right'] if 'right' in tree else None, level + 1)

@TestEngine.test 
def test_cliffs():
    if cliffs_delta([8,7,6,2,5,8,7,3],[8,7,6,2,5,8,7,3]) or not cliffs_delta([8,7,6,2,5,8,7,3],[9,9,7,8,10,9,6]):
        return False

    t1, t2 = [], []
    for i in range(1000):
        t1.append(rand())
        t2.append(pow(rand(), 0.5))
    
    if cliffs_delta(t1, t1) or not cliffs_delta(t1, t2):
        return False

    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x * j, t1))
        diff = cliffs_delta(t1, t3)
        print('> ' + str(rnd(j)) + ' ' + str(diff))
        j*= 1.025

    return True

@TestEngine.test 
def test_dist():
    data = Data('../../etc/data/auto93.csv')
    num = Num()
    num.txt = "test_dist Num"
    for i, row in enumerate(data.rows):
        num.add(data.dist(row, data.rows[1]))

    print(num.to_string()) #i have no idea if this is right. i can't find the expected output on menzie's repo
    return True

@TestEngine.test
def test_half():
    data = Data('../../etc/data/auto93.csv')
    half_res = data.half()
    print(str(len(half_res['left'])) + ", " + str(len(half_res['right'])))

    left, right = data.clone(half_res['left']), data.clone(half_res['right'])
    print(left.stats())
    print(right.stats())
    return True #todo (km) check these are correct

@TestEngine.test
def test_tree():
    data = Data('../../etc/data/auto93.csv')
    show_tree(data.tree(), 0) 
    return True

@TestEngine.test
def test_sway():
    data = Data('../../etc/data/auto93.csv')
    sway_res = data.sway()
    print('all: ' + str(data.stats()))
    print('best: ' + str(sway_res['best'].stats()))
    print('rest: ' + str(sway_res['rest'].stats()))
    return True

@TestEngine.test
def test_bin():
    data = Data('../../etc/data/auto93.csv')
    sway_res = data.sway()

    print('[all] best: ' + str(len(sway_res['best'].rows)) + ', rest: ' + str(len(sway_res['rest'].rows)))
    b4 = None
    for bin_res in data.bins(data.cols.x, sway_res):
        for range in bin_res:
            if range.txt != b4:
                print('')
            b4 = range.txt
            has = range.sources.has
            best_ratio = (has['best'] if 'best' in has else 0) / range.sources.n
            print(range.txt + ', ' + str(range.lo) + ', ' + str(range.hi) + ', ' + str(rnd(best_ratio)) + ', ' + str(range.sources.has))

    return True

@TestEngine.test
def test_resrvoir_sampling():
    current_max = Common.cfg['the']['Max']
    Common.cfg['the']['Max'] = 32

    num1 = Num()
    for i in range(10000):
        num1.add(i)


    Common.cfg['the']['Max'] = current_max #undo that change
    return len(num1.has) == 32


@TestEngine.test
def ALL():
    for k in Common.eg:
        if k != "ALL":
            print('\n' + "---------------------------------------")
            if not TestEngine.runs(k):
                Common.fails += 1
    return Common.fails == 0

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