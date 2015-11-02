import json
import os
import sys

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.abspath(os.path.join(MODULE_PATH, ".."))

CONFIG_PATH = os.path.join(BASE_PATH, "config")
DATA_PATH = os.path.join(BASE_PATH, "data")
LOG_PATH = os.path.join(BASE_PATH, "log")

LOGS = {"error": os.path.join(LOG_PATH, "error.txt"),
        "debug": os.path.join(LOG_PATH, "debug.txt"),}

config_filename = "config.json"
config_file = open(os.path.join(CONFIG_PATH, config_filename))

try:
    config_settings = json.load(config_file)
except Exception, e:
    print "Couldn't load settings: %s" %e
    sys.exit(1)

def get(key):
    return config_settings[key]