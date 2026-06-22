"""Module to update existing comics in database

Ideally this should
    1. find new comics.
    2. update statistics for existing comics.
    3. check for new chapters.
"""

import sqlite3
from datetime import datetime, UTC

import requests

from src.database.review import Review
from src.utilities import open_config, get_db_objs, get_api_headers
from src.jobs.initialize_data import gather_all_source_comics, create_comic
from src.scrapers.scraper import Scraper
from src.database.source import Source
from src.database.comic import Comic
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
    old_comics = ComicSource.get_all_by_source_id(cursor, source.obj_id)

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


def _update_reviews(comic: Comic, cursor: sqlite3.Cursor, comick_endpoint: str, comick_slug: str, timeout: str):
    old_reviews = comic.get_reviews()
    old_reviews_dict = {}
    for r in old_reviews:
        old_reviews_dict[r.user_name] = r

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
        user_name = r['identities']['traits']['username']

        old_review = old_reviews_dict.get(user_name, None)
        if not old_review: # Create the review.
            review = Review(cursor, comic.obj_id, user_name,
                            float(rating), r['content'], r['created_at'], r['updated_at'])
            review.create()
        else: # Update the review
            old_review.rating = float(rating)
            old_review.review_text = r['content']
            old_review.updated_at = r['updated_at']

            old_review.update()




def _update_statistics(comic: Comic, cursor: sqlite3.Cursor, comick_endpoint: str, timeout: int):
    print(f"Started updating stats for {comic.name}")

    now = datetime.now(UTC)
    status_dict = {
        1: "Ongoing",
        2: "Completed",
        3: "Cancelled",
        4: "Hiatus"
    }

    comic_request = requests.get(f"{comick_endpoint}/v1.0/search" \
                                f"?page=1&limit=15&showall=false&q={comic.name}&t=false",
                                timeout=timeout, headers=get_api_headers())
    if not comic_request.ok:
        print(f"Failed to fetch comic {comic.name} from Comick.dev: " \
            f"{comic_request.status_code} - {comic_request.text}")
        return None

    comic_data = comic_request.json()[0]

    comic.status = status_dict[comic_data['status']]
    comic.description = comic_data['desc']
    comic.chapter_count = comic_data['last_chapter']
    comic.rating = comic_data['bayesian_rating']
    comic.review_count = comic_data['rating_count']
    comic.last_updated = now

    _update_reviews(comic, cursor, comick_endpoint, comic_data['slug'], timeout)

    comic_sources = comic.get_comic_sources()
    for comic_source in comic_sources:
        source = comic_source.get_source()
        scraper = Scraper.get_scraper(source.class_name, source.base_url)

        scraped_comic = scraper.get_comic(comic_source.slug)

        if scraped_comic is None:
            print(f"SAD: Comic, {comic.name}, has been deleted on source, {scraper.name}, "\
                  "deleting Comic_Source reference.")
            comic_source.delete()
            continue

        comic_source.chapter_count = scraped_comic.chapter_count
        comic_source.status = scraped_comic.status
        comic_source.last_updated = now

        comic_source.update()


    comic.update()
    print(f"Finished updating stats for {comic.name}")


def update_data():
    """Entry function used to update all data"""

    Scraper.initialize_registry()

    config = open_config()
    cursor, con = get_db_objs()

    timeout = config['timeout']

    sources = _get_sources(cursor, timeout)
    for source in sources:
        _get_new_comics(source, cursor, timeout)

    comick_endpoint = config['comick_endpoint']

    comics = Comic.get_all(cursor)
    for comic in comics:
        _update_statistics(comic, cursor, comick_endpoint, timeout)

    con.commit()
    con.close()


if __name__ == "__main__":
    update_data()
