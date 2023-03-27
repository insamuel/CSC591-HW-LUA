import yaml
import Tests

from Utils import cli

import os

SCRIPTDIR = os.path.dirname(__file__)
YAMLFILE = os.path.join(SCRIPTDIR, 'config.yml')

##
# Loads a YAML configuration file "config.yml" into a Python dictionary
# "configs" using the yaml library.
#
# Prints usage information for the script and the options it supports.
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

help_string = """USAGE: stats.py [OPTIONS] [-g ACTION] \n OPTIONS:\n"
      "--bootstrap  bootstrap value                  = 512\n"
      "--cliffs     cliff's delta threshold          = 0.4\n"
      "--conf       conf value                       = 0.4\n"
      "--cohen      coehen value                     = 0.35\n"
      "-q  --quit  exit \n"""

print("stats.py\nenter --help for help.\n")

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

    if new_configs['the']['go']:
        Tests.ALL()
