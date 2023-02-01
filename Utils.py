from subprocess import call
import yaml
import math
import random

with open("config.yml", "r") as config_file:
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


def cli(args, configs):
    arg_arr = args.split(" ")

    run_tests = False
    if '-e' in arg_arr:
        run_tests = True
        arg_arr.remove("-e")

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

    if run_tests:
        call(["python", "/Tests.py"])

    return configs


def set_seed(x):
    configs['the']['seed'] = x