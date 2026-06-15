"""Utiltities module to be used globaly by other modules."""

import json

def open_config():
    """Opens the config file located in the base of this repository.
    
    Requires:
        * Nothing

    Returns:
        * A dictionary based on the json in conig.json
    """

    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)


def is_first_run():
    """Checks if this is the first run of the application.
    
    Requires:
        * Nothing
        
    Returns:
        * boolean
    """

    config = open_config()
    return config.get("first_run", True)


def set_first_run(value: bool):
    """Function used to set a value to the specified boolean value.
    
    Requires:
        value: bool

    Returns:
        * Nothing
    """

    config = open_config()
    config["first_run"] = value
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
