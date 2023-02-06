import yaml
import Tests
from Utils import cli

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
