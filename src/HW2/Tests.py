import Common
import sys
import TestEngine
from Num import Num
from Sym import Sym
from Data import Data
from Row import Row
from Utils import rnd, canPrint, rand, set_seed, read_csv


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
    row_count = 0
    def line_handler(xs: Row):
        nonlocal row_count
        row_count += 1
    read_csv(Common.cfg["the"]["file"], line_handler)
    return row_count == 399


@TestEngine.test
def eg_stats():
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
def ALL():
    for k in Common.eg:
        if k != "ALL":
            print('\n' + "---------------------------------------")
            if not TestEngine.runs(k):
                Common.fails += 1
    return True


if __name__ == "__main__":
    TestEngine.runs(Common.cfg["the"]["eg"])
    sys.exit(Common.fails)