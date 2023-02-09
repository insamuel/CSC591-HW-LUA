import copy as cp
from subprocess import call
import os
import csv

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
def read_csv(fname, fun=None):
    if fname is None or len(fname.strip()) == 0:
        raise Exception("File not found")
    else:

        #try to catch relative paths
        if not os.path.isfile(fname):
            fname = os.path.join(os.path.dirname(__file__), fname)

        fname = os.path.abspath(fname)

        csv_list = []
        with open(fname, 'r') as csv_file:
            csv_list = list(csv.reader(csv_file, delimiter=','))
        
        for item in csv_list:
            fun(item)

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


    def find_arg_value(args: list[str], optionA: str, optionB: str) -> str:
        index = args.index(optionA) if optionA in args else args.index(optionB)
        if (index + 1) < len(args):
            return args[index + 1]
        return None

    configs['the']['help'] = '-h' in args or '--help' in args
    configs['the']['go'] = '-g' in args or '--go' in args
    configs['the']['quit'] = '-q' in args or '--quit' in args
    configs['the']['dump'] = '-d' in args or '--dump' in args
    configs['the']['file'] = find_arg_value(args, '-f', '--file') if ('-f' in args or '--file' in args) else '../../etc/auto93.csv'
   
    #find the seed value
    if '-s' in args or '--seed' in args:
        seed_value = find_arg_value(args, '-s', '--seed')
        if seed_value is not None:
            try:
                configs['the']['seed'] = int(seed_value)
            except ValueError:
                raise ValueError("Seed value must be an integer!")
    else:
        configs['the']['seed'] = 937162211

    #find the far value
    if '-f' in args or '--far' in args:
        far_value = find_arg_value(args, '-f', '--far')
        if far_value is not None:
            try:
                configs['the']['far'] = float(far_value)
            except ValueError:
                raise ValueError("Far value must be a float!")
    else:
        configs['the']['far'] = 0.95

    #find the min value
    if '-m' in args or '--min' in args:
        min_value = find_arg_value(args, '-m', '--min')
        if min_value is not None:
            try:
                configs['the']['min'] = float(min_value)
            except ValueError:
                raise ValueError("Min value must be a float!")
    else:
        configs['the']['min'] = 0.5

    #find the p value
    if '-p' in args or '--p' in args:
        p_value = find_arg_value(args, '-p', '--p')
        if p_value is not None:
            try:
                configs['the']['p'] = int(p_value)
            except ValueError:
                raise ValueError("P value must be an integer!")
    else:
        configs['the']['p'] = 2
    
    #find the sample value
    if '-s' in args or '--sample' in args:
        sample_value = find_arg_value(args, '-s', '--sample')
        if sample_value is not None:
            try:
                configs['the']['sample'] = int(sample_value)
            except ValueError:
                raise ValueError("Sample value must be an integer!")
    else:
        configs['the']['sample'] = 512

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