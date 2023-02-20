import yaml
import Tests

from Utils import cli
import Repgrid

import os

SCRIPTDIR = os.path.dirname(__file__)
YAMLFILE = os.path.join(SCRIPTDIR, 'config.yml')

def run_repgrid(filepath: str):
    rep_rows = Repgrid.reprows(filepath)
    rep_cols = Repgrid.repcols(filepath)

    print('report for ' + filepath)
    print('======================= reprows =======================')
    Tests.show(rep_rows.cluster(), rep_rows.cols.all, 1, 0)
    
    
    print('\n======================= repcols =======================')
    Tests.show(rep_cols.cluster(), rep_cols.cols.all, 1, 0)

    print('\n======================= replace =======================')
    Repgrid.repplace(rep_rows)
    return True

##
# Loads a YAML configuration file "config.yml" into a Python dictionary
# "configs" using the yaml library.
#
# Prints usage information for the script and the options it supports (i
# e., -d, -g, -h, -s, -q).
#
# Runs an infinite loop (run_csv = True) to allow the user to input various
# options/arguments and update the configuration file "config.yml".
#
# If the 'help' field in the configuration file is set to True, it will
# print help text for the script's options.
#
# The "cli" function from the Utils module is used to process the user's
# input (stored in "csv_args") and update the "configs" dictionary
# accordingly.
#
# The updated "configs" dictionary is then written back to the "config.yml"
# file.
#
# The "Tests.ALL()" method is called, which runs a suite of tests
# for the script.
#
# The script allows the user to run a series of tests with
# different options/arguments and store the configuration in a YAML file.
##
with open(YAMLFILE, "r") as config_file:
    configs = yaml.safe_load(config_file)

help_string = """USAGE: grid.py [OPTIONS] [-g ACTION] \n OPTIONS:\n"
      " -d  --dump      on crash, dump stack        = false \n"
      "-f   --file      name of file                = ../../etc/data/auto93.cs\n"
      "-F   --Far       distance to \"faraway\"     = .95"
      "-g  --go         start-up action             = run all tests\n"
      "-r  --repgrid    run repgrid actions on file = false\n"
      "-h  --help       show help                   = false\n"
      "-p  --p          distance coefficient        = 2\n"
      "-m  --min        stop clusters at N^min = .5"
      "-s  --seed       random number seed          = 937162211 \n"
      "-q  --quit  exit \n"
      "-S  --Sample  sampling data size             = 512\n"""

print("grid.py : A rep grid processor. Enter -h/--help for help.\n")

run_csv = True

while run_csv:
    csv_args = input("Select an option/s \n")
    new_configs = cli(csv_args, configs)

    with open(YAMLFILE, "w") as config_file:
        config_file.write(yaml.dump(new_configs))

    if new_configs['the']['help']:
        print(help_string)

    if new_configs['the']['quit']:
        quit()

    if new_configs['the']['repgrid']:
        run_repgrid(new_configs['the']['file'])

    if new_configs['the']['go']:
        Tests.ALL()
