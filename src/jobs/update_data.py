"""Module to update existing comics in database

Ideally this should
    1. find new comics.
    2. update statistics for existing comics.
    3. check for new chapters.
"""

import sqlite3
from datetime import datetime, UTC

from src.utilities import open_config, get_db_objs
from src.jobs.initialize_data import gather_all_source_comics, create_comic
from src.scrapers.scraper import Scraper
from src.database.source import Source
from src.database.comic_source import ComicSource


def _get_sources(cursor: sqlite3.Cursor, timeout) -> list[Source]:
    config_sources = open_config()['scrapers']
    sources = Source.get_all(cursor)

    existing_source_names = {s.name for s in sources}
    for s in config_sources:
        if s['name'] not in existing_source_names:
            print(f"New scraper, {s['name']} detected. Adding comic information.")
            source = Source(cursor, name=s['name'], base_url=s['base_url'],
                            class_name=s["class_name"])
            source.create()

            gather_all_source_comics(source, cursor, timeout)
            sources.append(source)

    return sources


def _get_new_comics(source: Source, cursor: sqlite3.Cursor, timeout: int):
    scraper = Scraper.get_scraper(source.class_name, source.base_url)
    now = datetime.now(UTC)

    new_comics = scraper.get_all_comics()
    old_comics = ComicSource.get_all_by_source_id(cursor, source.id)

    if len(new_comics) > len(old_comics):
        print(f"New comic has been added to {source.name}. Beginning detection.")
        old_comic_names = [c.name for c in old_comic_names]
        for c in new_comics:
            if c.name not in old_comic_names:
                print(f"New comic, {c.name}, detected! Gathering details and creating entry.")

                c = c.get_details()
                comic = create_comic(c, now, cursor, timeout)

                source = Source.get(cursor, name=c.scraper.name)
                ComicSource(cursor, comic.obj_id, source.obj_id, c.chapter_count,
                            c.status, c.slug, now, now).create()


def update_data():
    """Entry function used to update all data"""

    Scraper.initialize_registry()

    config = open_config()
    cursor, con = get_db_objs()

    timeout = config['timeout']

    sources = _get_sources(cursor, timeout)
    for source in sources:
        _get_new_comics(source, cursor, timeout)

    con.execute()
    con.close()


if __name__ == "__main__":
    update_data()
