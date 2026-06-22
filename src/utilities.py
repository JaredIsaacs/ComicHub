"""Utiltities module to be used globaly by other modules."""

import json
import pathlib
import sqlite3

def get_base_directory() -> pathlib.Path:
    """Gets the base directory for the application.
    
    Requires:
        * Nothing
    Returns:
        * Base directory :)
    """
    return pathlib.Path(__file__).parent.resolve()


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


def get_db_objs() -> tuple[sqlite3.Cursor, sqlite3.Connection]:
    """Gets a cursor and con obj to the database using the db_name field in the config file.
    
    Requires:
        * Nothing
        
    Returns:
        * Cursor, Connection - Cursor and Connection objects"""
    config = open_config()

    con = sqlite3.connect(config['db_name'])
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    return cursor, con


def get_api_headers():
    """Function that returns api headers important for scraping.
    
    This allows us to get around basic bot detection.
    """

    config = open_config()
    comick_endpoint = config['comick_endpoint']

    return {
            "X-CSRF-Token": "",
            "Referer": f"{comick_endpoint}/",
            "Origin": comick_endpoint,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
