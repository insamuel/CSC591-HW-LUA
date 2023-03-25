import sys
import TestEngine
import Common
from Num import Num
from Utils import rnd, canPrint, rand, cliffs_delta, gaussian, samples

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
def test_gauss():
    t = []
    for i in range(10**4):
        t.append(gaussian(10,2))
    n=Num(t)
    print("\t", n.n, n.mu, n.sd)
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