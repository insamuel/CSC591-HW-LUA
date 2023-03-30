import random
import Common
import math
import yaml
import functools
from pathlib import Path

from Num import Num

##
# Imports call from subprocess, math, yaml and Path from pathlib
#
# Provides several functions and a class for test purposes. Includes
# functions for reading values from a YAML config file, generating
# pseudo-random numbers, type-casting strings to appropriate data types,
# reading CSV files, processing command-line arguments, etc. It also
# defines a custom exception class named "TestError" for raising exceptions
# in case of errors during tests.
##

##
# Retrieves the parent directory path of the current file and appends
# "config.yml" to it to create a config_path variable.
##
my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'config.yml'

##
# Opens the file at that path and uses the yaml.safe_load method to parse
# the YAML data in the file into a Python object configs. passer is
# assigned an empty string value.
##
with config_path.open() as config_file:
    configs = yaml.safe_load(config_file)


passer = ""

##
# Defines a custom exception class named "TestError". The class has an
# __init__ method that takes a string argument mess and assigns it to an
# instance variable self.mess. This custom exception can be raised and
# caught in a try-except block to handle specific error conditions in a
# program.
##
class TestError(Exception):
    def __init__(self, mess):
        self.mess = mess

##
# Defines a function "canPrint" which takes two arguments "content" and
# "mess". The function first tries to print the "content". If there is an
# exception raised while trying to print "content", it will raise a custom
# exception "TestError" with the message specified in the argument "mess".
##
def canPrint(content, mess):
    try:
        print(content)
    except:
        raise TestError(mess)

##
# Takes a string as an argument and returns a Boolean indicating whether
# the string can be converted to a floating-point number or not. If the
# string can be converted, the function returns True. If not, the function
# returns False.
##
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

##
# Defines a function "rand" that generates a pseudo-random number within a
# specified range (lo and hi). The number is generated based on a given
# seed value stored in the "configs" dictionary, which is multiplied by
# 16807 and then taken modulo 2147483647 to get the next seed. The
# generated number is then calculated by adding "lo" to the result of (hi -
# lo) multiplied by the seed value divided by 2147483647.
##
def rand(lo = None, hi = None):
    """
    Generates a pseudo-random number using seed.
    :param lo: Lower limit of generated number
    :param hi: Higher limit of generated number
    :return: Pseudo-random number
    """
    if not lo:
        lo = 0

    if not hi:
        hi = 1

    configs['the']['seed'] = (16807 * configs['the']['seed']) % 2147483647
    return lo + (hi - lo) * configs['the']['seed'] / 2147483647

def get_rand_items(list, item_count: int):
    return random.sample(list, item_count)

##
# Defines a function "rnd" that takes a floating point number x and an
# argument places, which sets the number of decimal places for the rounded
# result.
#
# It calculates the rounded value by multiplying x with 10 raised to the
# power of places, adding 0.5 to it. Then, rounding down to the nearest
# integer (floor), and then dividing it by the same value of 10 raised to
# the power of places. The rounded value is returned as the final result.
##
def rnd(x, places=2):
    mult = 10 ** places
    return math.floor(x * mult + 0.5) / mult

##
# Defines a function coerce that takes a string input s and converts it to
# its equivalent data type (either integer, boolean or string).
#
# The function coerce first checks if the input string s is a number by
# calling the function is_number. If s is a number, the function coerce
# returns a float representation of s. If s is not a number, the function
# returns None or the result of function fun with s as the argument.
##
def coerce(s):
    ##
    # Convert input in the form of a string to appropriate data type int
    # bool/str
    #
    # The function fun takes a string s1 as input and returns a
    # boolean value if the string is equal to "true" or "false". If s1 is
    # neither of those values, fun returns s1.
    ##
    def fun(s1):
        # returns boolean for the string
        if s == "true":
            return True
        elif s == "false":
            return False
        return s1

    ##
    # Return integer of the number in the form of string or calls fun to
    # return appropriately
    ##
    if is_number(s):
        return float(s)
    else:
        return None or fun(s)

def kap(list, func):
    res = {}
    for i, item in enumerate(list):
        ret = func(item)
        res[i] = ret
    return res

#find x,y from a line connecting `a` to `b`
def cos(a, b, c):
    denominator = 1 if c == 0 else 2 * c
    x1 = (pow(a, 2) + pow(c, 2) - pow(b, 2)) / denominator
    x2 = max(0, min(1, x1))
    y = pow(abs((pow(a, 2) - pow(x2, 2))), 0.5)
    return {'x': x2, 'y': y}

def per(t, p = 0.5):
    p = math.floor((p * len(t)) + 0.5)
    return t[max(1, min(len(t), p)) - 1]


##
# Function that processes command line arguments passed to the script. The
# function takes two arguments: args: A string of command line arguments
# separated by a space and configs: A dictionary that stores the
# configuration of the script.
#
# The function returns the updated configs dictionary
##
def cli(args, configs):
    arg_arr = args.split(" ")


    if '-e' in arg_arr:
        arg_arr.remove("-e")


    def find_arg_value(args: list[str], optionA: str, defaultValue) -> str:
        if optionA not in args:
            return defaultValue
        index = args.index(optionA)
        if (index + 1) < len(args):
            return args[index + 1]
        return None

    configs['the']['help'] = '-h' in args or '--help' in args
    configs['the']['go'] = '-g' in args or '--go' in args
    configs['the']['quit'] = '-q' in args or '--quit' in args
    configs['the']['bootstrap'] = float(find_arg_value(arg_arr, '--bootstrap', 512))
    configs['the']['conf'] = find_arg_value(arg_arr, '--conf', 0.05)
    configs['the']['cliffs'] = float(find_arg_value(arg_arr, '--cliffs', 0.4))
    configs['the']['cohen'] = float(find_arg_value(arg_arr,'--cohen', 0.35))

    return configs

def many(list, count):
    return random.choices(list, k = count)

def cliffs_delta(ns1, ns2):
    if len(ns1) > 128:
        ns1 = samples(ns1, 128)
    if len(ns2) > 128:
        ns2 = samples(ns2, 128)

    n, gt, lt = 0, 0, 0
    for item1 in ns1:
        for item2 in ns2:
            n+= 1
            if item1 > item2:
                gt+= 1
            if item1 < item2:
                lt+= 1
    
    return (abs(lt - gt) / n) <= Common.cfg['the']['cliffs']

def bootstrap(y0, z0):
    x = Num() # x will hold all of y0,z0
    y = Num() # y contains just y0
    z = Num() # z contains just z0

    for item in y0:
        y.add(item)
        x.add(item)
    for item in z0:
        z.add(item)
        x.add(item)

    xmu = x.mu
    ymu = y.mu
    zmu = z.mu

    yhat = []
    zhat = []
    # yhat and zhat are y,z fiddled to have the same mean
    for item in y0:
        yhat.append(item - ymu + xmu)
    for item in z0:
        zhat.append(item - zmu + xmu)

    # tobs is some difference seen in the whole space
    tobs = delta(y, z)
    n = 0
    for i in range(int(Common.cfg['the']['bootstrap'])):
        # here we look at some delta from just part of the space
        # it the part delta is bigger than the whole, then increment n
        if delta(Num(samples(yhat)), Num(samples(zhat))) > tobs:
            n+=1

    # if we have seen enough n, then we are the same
    return n / float(Common.cfg['the']['bootstrap']) >= float(Common.cfg['the']['conf'])

##
# Calculates an approximation of the error function, also known as the Gauss error function, for a
# given input x
##
def erf(x):
    # from Abramowitz and Stegun 7.1.26
    # https://s3.amazonaws.com/nrbook.com/AandS-a4-v1-2.pdf
    # (easier to read at https://en.wikipedia.org/wiki/Error_function#Approximation_with_elementary_functions)
    a1  = 0.254829592
    a2  = -0.284496736
    a3  = 1.421413741
    a4  = -1.453152027
    a5  = 1.061405429
    p   = 0.3275911

    # Save the sign of x
    sign = 1

    if x < 0:
        sign = -1

    x = math.abs(x)

    # A&S formula 7.1.26
    t = 1.0 / (1.0 + p*x)
    y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*math.exp(-x*x)

    return sign*y

##
# Returns a sample from a Gaussian with mean `mu` and sd `sd`
##
def gaussian(mu = 0, sd = 1):
    sq = math.sqrt
    pi = math.pi
    log = math.log
    cos = math.cos
    r = rand
    return mu + sd * sq(-2 * log(r())) * cos(2 * pi * r())


def samples(t, n=0):
    u = []
    n = n or len(t)
    for i in range(n):
        u.append(t[random.randrange(len(t))])

    return u

def delta(i, other):
    e, y, z = 1E-32, i, other
    return abs(y.mu - z.mu) / math.pow( (e + math.pow(y.sd, 2)/y.n + math.pow(z.sd, 2)/z.n), 0.5)


def RX(t, s = None):
    t.sort()
    return {"name": s or "", "rank": 0, "n": len(t), "show": "", "has": t}

##
# Returns mean of numbers added.
##
def mid(t):
    t = t["has"] if "has" in t else t
    n = len(t) // 2
    return len(t) % 2 == 0 and (t[n] + t[n + 1]) / 2 or t[n + 1]

##
# Returns standard deviation of numbers added.
##
def div(t):
    t = t["has"] if "has" in t else t
    return (t[len(t) * 9 // 10] - t[len(t) * 1 // 10]) / 2.56


def merge(rx1, rx2):
    rx3 = RX([], rx1["name"])
    for t in (rx1["has"], rx2["has"]):
        for x in t:
            rx3["has"].append(x)
    rx3["has"].sort()
    rx3["n"] = len(rx3["has"])
    return rx3


def scott_knot(rxs):
    def merges(i, j):
        out = RX([], rxs[i]["name"])
        for k in range(i, j + 1):
            out = merge(out, rxs[j])
        return out

    def same(lo, cut, hi):
        l = merges(lo, cut)
        r = merges(cut + 1, hi)
        x = cliffs_delta(l["has"], r["has"])
        if x == True:
            return bootstrap(l["has"], r["has"])
        else:
            return x

    def recurse(lo, hi, rank):
        cut = None
        b4 = merges(lo, hi)
        best = 0
        for j in range(lo, hi):
            if j < hi:
                l = merges(lo, j)
                r = merges(j + 1, hi)
                now = (l["n"] * (mid(l) - mid(b4)) ** 2 + r["n"] * (mid(r) - mid(b4)) ** 2) / (l["n"] + r["n"])
                if now > best:
                    if abs(mid(l) - mid(r)) > cohen:
                        cut, best = j, now
        if cut and not same(lo, cut, hi):
            rank = recurse(lo, cut, rank) + 1
            rank = recurse(cut + 1, hi, rank)
        else:
            for i in range(lo, hi):
                rxs[i]["rank"] = rank
        return rank

    rxs.sort(key=lambda x: mid(x))
    cohen = div(merges(0, len(rxs) - 1)) * Common.cfg['the']['cohen']
    recurse(0, len(rxs) - 1, 1)
    return rxs


def tiles(rxs):
    huge, min_f, max_f, floor = float("inf"), min, max, math.floor
    lo, hi = huge, -huge
    for rx in rxs:
        lo = min_f(lo, rx["has"][0])
        hi = max_f(hi, rx["has"][-1])
    for rx in rxs:
        t, u = rx["has"], []

        def of(x, most):
            return max(0, min_f(most, x))

        def at(x):
            return t[of(int(len(t) * x), len(t) - 1)]

        def pos(x):
            return floor(of(Common.cfg['the']['width'] * (x - lo) / (hi - lo + 1E-32) // 1, Common.cfg['the']['width']))

        for _ in range(Common.cfg['the']['width']):
            u.append(" ")
        a, b, c, d, e = at(.1), at(.3), at(.5), at(.7), at(.9)
        A, B, C, D, E = pos(a), pos(b), pos(c), pos(d), pos(e)
        for i in range(A, B):
            u[i] = "-"
        for i in range(D, E):
            u[i] = "-"

        u[(Common.cfg['the']['width'] // 2) - 1] = "|"
        u[C] = "*"
        rx["show"] = "".join(u) + " { %6.2f" % a + "}"
        for x in (b, c, d, e):
            rx["show"] += ", %6.2f" % x
        rx["show"] += " }"
    return rxs