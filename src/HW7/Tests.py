import sys
import TestEngine
import Common
from Num import Num
from Utils import rnd, canPrint, rand, cliffs_delta, gaussian, samples, bootstrap

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

@TestEngine.test
def test_gauss():
    t = []
    for i in range(10**4):
        t.append(gaussian(10,2))
    n=Num(t)
    print("\t", n.n, n.mu, n.sd)
    return True


@TestEngine.test
def test_basic():
    listA = [8, 7, 6, 2, 5, 8, 7, 3]
    listB = [9, 9, 7, 8, 10, 9, 6]

    listC = [0.34, 0.49, 0.51, 0.6, .34, .49, .51, .6]
    listD = [0.6,  0.7,  0.8, 0.9, .6, .7, .8, .9]

    print('\t\tTrue\t' + str(bootstrap(listA, listA)) + '\t' + str(cliffs_delta(listA, listA)))
    print('\t\tFalse\t' + str(bootstrap(listA, listB)) + '\t' + str(cliffs_delta(listA, listB)))
    print('\t\tFalse\t' + str(bootstrap(listC, listD)) + '\t' + str(cliffs_delta(listC, listD)))
    
    return True



@TestEngine.test
def test_num():
    n = Num([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(n.n, n.mu, n.sd)
    return True


@TestEngine.test
def test_sample():
    for i in range(1,10):
        print("\t" + "".join(samples(["a","b","c","d","e"])))

    return True


@TestEngine.test
def test_bootstrap():
    a = []
    b = []
    for i in range(100):
        a.append(gaussian(10, 1))
    print('\tmu\tsd\tcliffs\tboot\tboth')
    print('\t--\t--\t------\t----\t----')

    mu = 10.0
    for i in range(11):
        b.append(gaussian(mu, 1))
    
        cl = cliffs_delta(a, b)
        bs = bootstrap(a, b)
        print('\t' + str(rnd(mu, 1)) + '\t1\t' + str(cl) + '\t' + str(bs) + '\t' + str(cl and bs))
        
        mu+= 0.1
    return True

@TestEngine.test
def test_pre():
    print("eg3")
    d = 1
    for i in range(10):
        t1 = []
        t2 = []
        for j in range(32):
            t1.append(gaussian(10, 1))
            t2.append(gaussian(d * 10, 1))
        print('\t' + str(rnd(d)) + '\t' + str(d < 1.1) + '\t' + str(bootstrap(t1, t2)) + '\t' + str(bootstrap(t1, t1)))
        d+= 0.5
    return True
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