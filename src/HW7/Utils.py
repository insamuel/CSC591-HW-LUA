import random
import Common
import math
import yaml
from pathlib import Path

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


    def find_arg_value(args: list[str], optionA: str, optionB: str, defaultValue) -> str:
        if optionA not in args and optionB not in args:
            return defaultValue
        index = args.index(optionA) if optionA in args else args.index(optionB)
        if (index + 1) < len(args):
            return args[index + 1]
        return None

    configs['the']['help'] = '-h' in args or '--help' in args
    configs['the']['go'] = '-g' in args or '--go' in args
    configs['the']['quit'] = '-q' in args or '--quit' in args
    configs['the']['bins'] = float(find_arg_value(arg_arr, '-b', '--bins', 16))
    configs['the']['file'] = find_arg_value(arg_arr, '-f', '--file', '../../etc/data/auto93.csv')
    configs['the']['cliffs'] = float(find_arg_value(arg_arr, '-c', '--cliffs', 0.147))
    configs['the']['Far'] = float(find_arg_value(arg_arr, '-F', '--Far', 0.95))
    configs['the']['Halves'] = float(find_arg_value(arg_arr, '-H', '--Halves', 512))
    configs['the']['min'] = float(find_arg_value(arg_arr, '-m', '--min', 0.5))
    configs['the']['Max'] = int(find_arg_value(arg_arr, '-M', '--Max', 512))
    configs['the']['p'] = int(find_arg_value(arg_arr, '-p', '--p', 2))
    configs['the']['rest'] = int(find_arg_value(arg_arr, '-r', '--rest', 4))
    configs['the']['Reuse'] = bool(find_arg_value(arg_arr, '-R', '--Reuse', True))
    configs['the']['seed'] = float(find_arg_value(arg_arr, '-s', '--seed', 937162211))

    return configs

def many(list, count):
    return random.choices(list, k = count)

def cliffs_delta(nsA, nsB):
    if len(nsA) > 256:
        nsA = many(nsA, 256)
    if len(nsB) > 256:
        nsB = many(nsB, 256)
    if len(nsA) > 10 * len(nsB):
        nsA = many(nsA, 10 * len(nsB))
    if len(nsB) > 10 * len(nsA):
        nsB = many(nsB, 10 * len(nsA))

    n, gt, lt = 0, 0, 0
    for itemA in nsA:
        for itemB in nsB:
            n+= 1
            if itemA > itemB:
                gt+= 1
            if itemA < itemB:
                lt+= 1
    
    return (abs(lt - gt) / n) > Common.cfg['the']['cliffs']


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
    r = random.random
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
def mid(self, t):
    t = t["has"] if "has" in t else t
    n = len(t) // 2
    return len(t) % 2 == 0 and (t[n] + t[n + 1]) / 2 or t[n + 1]

##
# Returns standard deviation of numbers added.
##
def div(self, t):
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