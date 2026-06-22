'''
Module for initializing data into the database.

This should dynamically pick up and Scraper class that exists in the config and the scraper folder.
Then cross reference that data with the Comick api.

    Step 1: scrape all sources.
    Step 2: Find their Comick.dev version
    Step 3: prophit
'''

import sqlite3
from datetime import datetime, UTC

from dotenv import load_dotenv
import requests

from src.utilities import open_config, get_db_objs, get_api_headers
from src.database.initialize_database import initialize_database
from src.scrapers.scraper import Scraper
from src.scrapers import comic as ScraperComic
from src.database.tag import Tag
from src.database.genre import Genre
from src.database.comic import Comic
from src.database.comic_source import ComicSource
from src.database.source import Source
from src.database.alt_name import AltName
from src.database.review import Review

load_dotenv()

def _populate_tags(cursor: sqlite3.Cursor, timeout: int):
    config = open_config()
    comick_endpoint = config['comick_endpoint']

    url = f"{comick_endpoint}/category/"
    response = requests.get(url, timeout=timeout)
    if not response.ok:
        raise ConnectionError("Failed to fetch categories: " \
                            f"{response.status_code} - {response.text}")

    categories = response.json()
    for c in categories:
        tag = Tag(cursor, name=c['title'])
        tag.create()


def _populate_genres(cursor: sqlite3.Cursor, timeout: int):
    config = open_config()
    comick_endpoint = config['comick_endpoint']

    url = f"{comick_endpoint}/genre/"
    response = requests.get(url, timeout=timeout)
    if not response.ok:
        raise ConnectionError("Failed to fetch categories: "\
                            f"{response.status_code} - {response.text}")

    genres = response.json()
    for g in genres:
        genre = Genre(cursor, name=g['name'], genre_group=g['group'], obj_id=g['id'])
        genre.create()


def _populate_sources(cursor: sqlite3.Cursor):
    config = open_config()

    for s in config['scrapers']:
        try:
            source = Source(cursor, name=s['name'],
                            base_url=s['base_url'], class_name=s['class_name'])
            source.create()
        except sqlite3.IntegrityError:
            print(f"Source {s['name']} already exists in the database.")


def create_comic(source_comic: ScraperComic, time: str,
                cursor: sqlite3.Cursor, timeout: int) -> Comic | None:
    '''Creates a comic provided a ScraperComic object.

    Requires:
        * source_comic: ScraperComic - object to add :).
        * time: str - time str that determins the initial added/updated date.
        * cursor: sqlite3.Cursor - used to connect to the db.
        * timout: int - determines when to call it quits for http requests.

    Returns.
        * Nothing

    '''

    def _create_alt_titles(cursor: sqlite3.Cursor, comick_data, comic_id: int):
        for t in comick_data['md_titles']:
            alt_name = AltName(cursor, comic_id, t['title'])
            alt_name.create()

    def _create_reviews(cursor: sqlite3.Cursor, comick_slug: str, comic_id: int):
        config = open_config()
        comick_endpoint = config['comick_endpoint']
        reviews_request = requests.get(f"{comick_endpoint}/comic/{comick_slug}",
                                        timeout=timeout, headers=get_api_headers())
        if not reviews_request.ok:
            print(f"Failed to fetch reviews for {comick_slug} " \
                "from Comick.dev: {reviews_request.status_code} - {reviews_request.text}")
            return 

        reviews_data = reviews_request.json()
        for r in reviews_data['comic']['reviews']:
            rating = r['rating']
            if not rating:
                rating = 0

            review = Review(cursor, comic_id, r['identities']['traits']['username'],
                            float(rating), r['content'], r['created_at'], r['updated_at'])
            review.create()

    def _gather_genres(comick_data):
        tags = []
        for g in comick_data['genres']:
            genre = Genre.get(cursor, obj_id=g)
            tags.append(genre)

        return tags

    config = open_config()
    comick_endpoint = config['comick_endpoint']
    status_dict = {
        1: "Ongoing",
        2: "Completed",
        3: "Cancelled",
        4: "Hiatus"
    }

    comic_request = requests.get(f"{comick_endpoint}/v1.0/search" \
                                f"?page=1&limit=15&showall=false&q={source_comic.name}&t=false",
                                timeout=timeout, headers=get_api_headers())
    if not comic_request.ok:
        print(f"Failed to fetch comic {source_comic.name} from Comick.dev: " \
            f"{comic_request.status_code} - {comic_request.text}")
        return None

    comic_data = comic_request.json()[0]

    comic = Comic(
        cursor,
        source_comic.name,
        source_comic.cover_image_url,
        status_dict[comic_data['status']],
        comic_data['desc'],
        source_comic.chapter_count,
        comic_data['bayesian_rating'],
        comic_data['rating_count'],
        time,
        time,
        comic_data['year']
    )

    comic.create()

    _create_alt_titles(cursor, comic_data, comic.obj_id)
    _create_reviews(cursor, comic_data['slug'], comic.obj_id)

    genres = _gather_genres(comic_request.json()[0])
    for g in genres:
        g.associate_comic(comic.obj_id)

    return comic


def gather_all_source_comics(source: Source, cursor: sqlite3.Cursor, timeout: int):
    '''Gathers all comics associated to a source, and creates them if there is a new one.

    Essentially the function that associates source to comics.
    Might be a better idea to rename it to that.

    Requires:
        * source: Source - the source object used to gather comics.
        * cursor: sqlite3.Cursor - how we connect to the db.
        * timout: how long we will allow the connection to hang before killing it.

    Returns:
        * Nothing.
    '''

    now = datetime.now(UTC)

    scraper = Scraper.get_scraper(source.class_name, source.base_url)
    comics = scraper.get_all_comics()

    for c in comics:
        c = c.get_details()

        comic = Comic.get(cursor, name=c.name)
        if comic:
            print(f"Comic {c.name} already exists in the database (found {comic.name}). " \
                "Skipping creation.")
            continue

        comic = create_comic(c, now, cursor, timeout)
        source = Source.get(cursor, name=c.scraper.name)
        ComicSource(cursor, comic.obj_id, source.obj_id, c.chapter_count, c.status,
                    c.slug, now, now).create()

    return comics


def initialize_data():
    """Function used to initialize a brand new database."""

    Scraper.initialize_registry()

    config = open_config()
    cursor, con = get_db_objs()

    timeout = config['timeout']

    initialize_database(cursor)
    _populate_tags(cursor, timeout)
    _populate_genres(cursor, timeout)
    _populate_sources(cursor)

    for s in config['scrapers']:
        gather_all_source_comics(Source.get(cursor, name=s['name']), cursor, timeout)

    con.commit()
    con.close()

if __name__ == "__main__":
    initialize_data()
