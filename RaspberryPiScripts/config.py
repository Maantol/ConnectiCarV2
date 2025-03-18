import json

def load_config():
    with open("config.json", "r") as file:
        config = json.load(file)
        print("config: ", config)
    return config

config = load_config()

def get_config():
    return config