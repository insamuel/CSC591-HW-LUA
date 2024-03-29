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

@TestEngine.test
def eg_duplicate_structure():
    d1 = Data(Common.cfg['the']['file'])
    d2 = d1.clone()
    return len(d1.rows) == len(d2.rows) and d1.cols.y[1].w == d2.cols.y[1].w and d1.cols.y[1].at == d2.cols.y[1].at

@TestEngine.test 
def test_data():
    # i know this is horrible but it works
    expected_output = '\ny\tmid\t{ :Lbs- 2970.42 :Acc+ 15.57 :Mpg+ 23.84}\n \tdiv\t{ :Lbs- 846.84 :Acc+ 2.76 :Mpg+ 8.34}\nx\tmid\t{ :Clndrs 5.45 :Volume 193.43 :Model 76.01 :origin 1}\n \tdiv\t{ :Clndrs 1.7 :Volume 104.27 :Model 3.7 :origin 1.3273558482394003}'
    test_data = Data('../../etc/data/auto93.csv')
    
    y_mid_report = '{'
    y_div_report = '{'
    for y in test_data.cols.y:
        y_mid_report = y_mid_report + ' :' + y.txt + ' ' + str(y.rnd(y.mid(), 2))
        y_div_report = y_div_report + ' :' + y.txt + ' ' + str(y.rnd(y.div(), 2))
    y_mid_report = y_mid_report + '}'
    y_div_report = y_div_report + '}'

    x_mid_report = '{'
    x_div_report = '{'
    for x in test_data.cols.x:
        x_mid_report = x_mid_report + ' :' + x.txt + ' ' + str(x.rnd(x.mid(), 2))
        x_div_report = x_div_report + ' :' + x.txt + ' ' + str(x.rnd(x.div(), 2))
    x_mid_report = x_mid_report + '}'
    x_div_report = x_div_report + '}'

    res_string = '\ny\tmid\t' + y_mid_report + '\n \tdiv\t' + y_div_report + '\nx\tmid\t' + x_mid_report + '\n \tdiv\t' + x_div_report
    print(res_string)
    return res_string == expected_output

@TestEngine.test
def test_sort_nearest_neighbor():
    data = Data('../../etc/data/auto93.csv')
    around_res = data.around(data.rows[0])

    expected_output = "0\t0.0\t['8', '304.0', '193', '4732', '18.5', '70', '1', '10']\n50\t0.17\t['8', '318', '150', '4457', '13.5', '74', '1', '10']\n100\t0.28\t['6', '232', '100', '2901', '16', '74', '1', '20']\n150\t0.38\t['8', '351', '142', '4054', '14.3', '79', '1', '20']\n200\t0.55\t['4', '122', '96', '2300', '15.5', '77', '1', '30']\n250\t0.68\t['4', '119', '82', '2720', '19.4', '82', '1', '30']\n300\t0.71\t['4', '119', '97', '2545', '17', '75', '3', '20']\n350\t0.79\t['4', '146', '67', '3250', '21.8', '80', '2', '30']\n"
    res_string = ""
    for i in range(len(around_res)):
        if i % 50 == 0:
            row = around_res[max(0, i -1)]
            dist = rnd(data.dist(row, data.rows[0]), 2)
            res_string+= str(i) + "\t" + str(dist) + '\t' + str(row.cells) + '\n'
    print(res_string)
    return expected_output == res_string

@TestEngine.test
def test_one_level_bi_clustering():
    data = Data('../../etc/data/auto93.csv')
    set_seed(937162211)
    half_res = data.half()
    res_string = str(len(half_res['left'])) + '\t' + str(len(half_res['right'])) + '\t' + str(len(data.rows)) + '\n'
    res_string += str(half_res['A'].cells) + '\t' + str(half_res['c']) + '\n'
    res_string+= str(half_res['mid'].cells) + '\n'
    res_string+= str(half_res['B'].cells) + '\n'
    print(res_string)

    expected_res = "199\t199\t398\n['4', '90', '48', '1985', '21.5', '78', '2', '40']\t0.6393183441778267\n['4', '151', '90', '2950', '17.3', '82', '1', '30']\n['6', '232', '100', '2634', '13', '71', '1', '20']\n"
    return res_string == expected_res

def show(cluster_res, cols, n_places, level):
    if cluster_res != None:
        report_string = ('| '*level)

        data = cluster_res['data']

        report_string+= ' ' + str(len(data.rows))
        if 'left' not in cluster_res or level == 0:
            report_string+= ' { '
            for y in data.cols.y:
                report_string+= ' :' + y.txt + ' ' + str(y.rnd(y.mid(), n_places))
            report_string+= ' }'
        print(report_string)

        show(cluster_res['left'] if 'left' in cluster_res else None, cols, n_places, level + 1)
        show(cluster_res['right'] if 'right' in cluster_res else None, cols, n_places, level + 1)


@TestEngine.test
def test_cluster():
    data = Data('../../etc/data/auto93.csv')

    show(data.cluster(), data.cols.y, 1, 0)

    return True

@TestEngine.test
def test_sway():
    data = Data('../../etc/data/auto93.csv')
    show(data.sway(), data.cols.y, 1, 0)

    return True

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