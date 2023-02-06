import Common
import sys
import TestEngine
from Num import Num
from Sym import Sym
from Data import Data
from Utils import rnd, canPrint, rand, set_seed, csv


@TestEngine.test
def eg_the():
    canPrint(Common.cfg['the'], 'Should be able to print the')
    return True


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


@TestEngine.test
def eg_sym():
    s = Sym()

    test_vals = ["a", "a", "a", "a", "b", "b", "c"]

    for x in test_vals:
        s.add(x)

    mode, entropy = s.mid(), rnd(s.div(), 3)
    results = "mid= {}, div= {}".format(mode, entropy)
    canPrint(results, 'Should be able to print mid and div')

    return mode == "a" and 1.379 == entropy


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
def eg_data():
    data = Data(Common.cfg['the']['file'])

    return len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and len(data.cols.x) == 4


@TestEngine.test
def eg_csv():
    def fun(row):
        fun.n += len(row)
        if fun.n < 8 * 25:
            canPrint(row, 'Should be able to print rows')

    fun.n = 0
    csv(Common.cfg['the']['file'], fun)
    return fun.n == 8 * 399


@TestEngine.test
def eg_stats():
    def div(col):
        if type(col) == Num:
            return Num.div(col)
        else:
            return Sym.div(col)

    def mid(col):
        if type(col) == Num:
            return Num.mid(col)
        else:
            return Sym.mid(col)

    data = Data(Common.cfg['the']['file'])
    print('xmid', end='\t')
    canPrint(data.stats(mid, data.cols.x, 2), 'xmid')
    print('xdiv', end='\t')
    canPrint(data.stats(div, data.cols.x, 3), 'xdiv')
    print('ymid', end='\t')
    canPrint(data.stats(mid, data.cols.y, 2), 'ymid')
    print('ydiv', end='\t')
    canPrint(data.stats(div, data.cols.x, 3), 'ydiv')
    return True



@TestEngine.test
def ALL():
    for k in Common.eg:
        if k != "ALL":
            print("\n−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−")
            if not TestEngine.runs(k):
                Common.fails += 1
    return True


if __name__ == "__main__":
    TestEngine.runs(Common.cfg["the"]["eg"])
    sys.exit(Common.fails)