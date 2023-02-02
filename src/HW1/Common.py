import yaml
from pathlib import Path

my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'config.yml'

with config_path.open() as config_file:
    cfg = yaml.safe_load(config_file)

eg = {}
fails = 0
