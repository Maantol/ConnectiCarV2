import json
import os

def load_config():

    #loads config from folder
    config_file_path = os.path.join(os.path.dirname(__file__), 'config', 'config.json')

    with open(config_file_path, "r") as file:
        config = json.load(file)
        print("Config: ", json.dumps(config, indent=4))
    return config

config = load_config()

def get_config():
    return config