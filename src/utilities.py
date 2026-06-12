import json

def open_config():
    with open("config.json", "r") as f:
        return json.load(f)
    

def is_first_run():
    config = open_config()
    return config.get("first_run", True)


def set_first_run(value: bool):
    config = open_config()
    config["first_run"] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)