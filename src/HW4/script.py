import yaml
import Tests
from Utils import cli

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
with open("config.yml", "r") as config_file:
    configs = yaml.safe_load(config_file)

print("main.py : an example script with help text and a test suite\n")
print("USAGE: main.py [OPTIONS] [-g ACTION] \n OPTIONS:\n"
      " -d  --dump  on crash, dump stack = false \n"
      " -g  --go    start-up action      = data\n"
      " -h  --help  show help            = false\n" 
      " -s  --seed  random number seed   = 937162211 \n"
      " -q  --quit  exit \n")

run_csv = True

while run_csv:
    if configs['the']['help']:
        print("Help \n USAGE EX: -s 456765 -g data \n OPTIONS:\n"
              " -d  --dump  on crash, dump stack = false \n"
              " -g  --go    start-up action      = data\n"
              " -h  --help  show help            = false\n" 
              " -s  --seed  random number seed   = 937162211 \n"
              " -q  --quit  exit \n")
    csv_args = input("Select an option/s \n")
    new_configs = cli(csv_args, configs)

    with open("config.yml", "w") as config_file:
        config_file.write(yaml.dump(new_configs))

    Tests.ALL()
