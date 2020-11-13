import os
import json

from pathlib import Path

try:
  environment = os.environ['RELE_ENV']
except KeyError:
  environment = 'local'

default_environemnt = json.load(Path(__file__).parent / 'env.default.json')
local_path = Path(__file__).parent / f'env.{environment}.json'
if local_path.exists():
  local_environemnt = json.load(local_path)
else:
  local_environemnt = {}

def get_option(option: str) -> any:
  # check os.environ
  # check local config
  # check default config
  environment_name = f'RELE_{option.upper()}'
  try:
    return os.environ[environment_name]
  except KeyError:
    pass
  try:
    return local_environemnt[option]
  except KeyError:
    pass
  return default_environemnt[option]

