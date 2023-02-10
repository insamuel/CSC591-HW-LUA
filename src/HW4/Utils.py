import copy as cp
from subprocess import call
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
def rand(lo, hi):
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


##
# Call "fun" on each row. Row cells are divided in "the.seperator"
#
# Defines a function csv(fname, fun=None), which reads a CSV (Comma
# Separated Values) file specified by fname, typecasts every cell in each
# row to appropriate data type (int, bool or str) using the coerce()
# function, and applies the function fun to every row of the CSV file, if
# fun is specified.
#
# If fname is None or an empty string, an Exception is raised with message
# "File not found". The separator used to split a row is specified in
# Common.cfg['the']['separator']. The new line (\n) at the end of each row
# is removed before typecasting the cells.
##
def csv(fname, fun=None):
    if fname is None or len(fname.strip()) == 0:
        raise Exception("File not found")
    else:
        sep = ","
        file_path = my_path.parent.parent.parent / "etc" / fname
        with open(file_path, 'r') as s:
            for s1 in s.readlines():
                t = []
                csv_row = s1.split(sep)             # Split a row using the separator, here ','
                csv_row[-1] = csv_row[-1][:-1]      # Removing \n from the end of last element
                for cell in csv_row:
                    t.append(coerce(cell))          # Every cell should be type casted
                if fun:
                    fun(t)

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

    ##
    # The input string of arguments is split into an array of strings called
    # arg_arr. A variable run_tests is set to False and will be set to True
    # if the argument "-e" is found in arg_arr.
    ##
    run_tests = False
    if '-e' in arg_arr:
        run_tests = True
        arg_arr.remove("-e")

    ##
    # The function then loops through the arg_arr array with a step size of
    # 2.
    #
    # If the current element in the loop is "-d", the next element is
    # processed to set the 'dump' key in the configs dictionary.
    #
    # If the current element in the loop is "-g", the next element is
    # processed to set the 'go' key in the configs dictionary.
    #
    # If the current element in the loop is "-h", the next element is
    # processed to set the 'help' key in the configs dictionary.
    #
    # If the current element in the loop is "-s", the next element is
    # processed as an integer to set the seed for the script.
    #
    # If the current element in the loop is "-q", the function prints
    # "Exiting." and immediately exits the program.
    ##
    for x in range(0, len(arg_arr), 2):
        if arg_arr[x] == "-d":
            if arg_arr[x + 1] == 'True' or arg_arr[x + 1] == 'true':
                configs['the']['dump'] = True
            else:
                configs['the']['dump'] = False
            continue
        elif arg_arr[x] == "-g":
            configs['the']['go'] = str(arg_arr[x + 1])
            continue
        elif arg_arr[x] == "-h":
            if arg_arr[x + 1] == 'True' or arg_arr[x + 1] == 'true':
                configs['the']['help'] = True
            else:
                configs['the']['help'] = False
            continue
        elif arg_arr[x] == "-s":
            set_seed(int(arg_arr[x + 1]))
            continue
        elif arg_arr[x] == "-q":
            print("Exiting.")
            exit()
        else:
            print(args[x], " is not a valid option. Exiting.")
            exit()

    ##
    # If the run_tests flag was set to True, the function will call the
    # script Tests.py.
    ##
    if run_tests:
        call(["python", "/Tests.py"])

    return configs

##
# Function sets the value of seed in the dictionary configs['the'] to x.
# The configs dictionary holds the configuration data and the seed key in
# it holds the value for a seed used for generating random numbers. This
# function sets the value of seed to x.
##
def set_seed(x):
    configs['the']['seed'] = x

def copy(t):
    return cp.deepcopy(t)