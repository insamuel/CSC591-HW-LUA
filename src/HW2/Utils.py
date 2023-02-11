from subprocess import call
import os
import csv
import random

import Common
import math
import yaml
from pathlib import Path

my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'config.yml'

with config_path.open() as config_file:
    configs = yaml.safe_load(config_file)

passer = ""


class TestError(Exception):
    def __init__(self, mess):
        self.mess = mess


def canPrint(content, mess):
    try:
        print(content)
    except:
        raise TestError(mess)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


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


def rnd(x, places=2):
    mult = 10 ** places
    return math.floor(x * mult + 0.5) / mult


def coerce(s):
    # convert input in the form of a string to appropriate data type int/bool/str
    def fun(s1):
        # returns boolean for the string
        if s == "true":
            return True
        elif s == "false":
            return False
        return s1

    # return integer of the number in the form of string or calls fun to return appropriately
    if is_number(s):
        return float(s)
    else:
        return None or fun(s)


# Call "fun" on each row. Row cells are divided in "the.seperator"
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
        
        if fun != None:
            for item in csv_list:
                fun(item)


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
    configs['the']['file'] = find_arg_value(args, '-f', '--file') if ('-f' in args or '--file' in args) else '../../etc/data/auto93.csv'
   
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

    return configs


def set_seed(x):
    configs['the']['seed'] = x