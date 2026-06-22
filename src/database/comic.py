"""Module used for interacting with or accessing with the Comic table."""

from sqlite3 import Cursor
from datetime import datetime

from src.database.comic_source import ComicSource
from src.database.database_row import DatabaseRow
from src.database.review import Review


class Comic(DatabaseRow):
    """Represents the actual Comic object from the database.
    Which has data collected from either the Source or the Comick API.

    Special methods:
        search(cursor: Cursor, query: str) -> list[Comic]:
        This is going to be used for the search bar feature.

        Returns comics from the db that are similar to a query string. Include objects from the
        Alt_Name table.
    """
    def __init__(self, cursor: Cursor, name: str, cover_image_url: str, status: str,
                description: str, chapter_count: float, rating: float, review_count:int,
                date_added: datetime, last_updated: datetime, year_published: int,
                obj_id : int | None = None):
        super().__init__(cursor, obj_id)

        self.name = name
        self.cover_image_url = cover_image_url
        self.status = status
        self.description = description
        self.chapter_count = chapter_count
        self.rating = rating
        self.review_count = review_count
        self.date_added = date_added
        self.last_updated = last_updated
        self.year_published = year_published


    @staticmethod
    def get(cursor: Cursor, obj_id: int = None, name: str = None) -> Comic | None:
        if obj_id is None and name is None:
            raise ValueError("Both name and id cannot be None!")

        if obj_id is not None:
            query = "SELECT * FROM Comic WHERE id = ?"
            cursor.execute(query, (obj_id,))
        else:
            query = "SELECT * FROM Comic LEFT JOIN AltName ON Comic.id = AltName.comic_id " \
            "WHERE Comic.name = ? OR AltName.alt_name = ?"
            cursor.execute(query, (name, name))

        row = cursor.fetchone()
        if not row:
            return None

        return Comic(cursor, row['name'], row['cover_image_url'], row['status'], row['description'],
                    row['chapter_count'], row['rating'], row['review_count'], row['date_added'],
                    row['last_updated'], row['year_published'], row['id'])


    @staticmethod
    def get_all(cursor: Cursor) -> list[Comic]:
        '''
        Accepts:
            * cursor: Cursor
        
        Returns:
            All comics in the comics table.
        '''

        sql_query = "SELECT * FROM Comic"
        response = cursor.execute(sql_query)

        comics = []
        for data in response.fetchall():
            comics.append(Comic(cursor, data['name'], data['cover_image_url'], data['status'],
                                data['description'], data['chapter_count'], data['rating'],
                                data['review_count'], data['date_added'], data['last_updated'],
                                data['year_published'], data['id']))
        
        return comics


    @staticmethod
    def search(cursor: Cursor, query: str) -> list[Comic]:
        '''
        Accepts:
            * cursor: Cursor
            * query: str

        Returns:
            Comics that have names or altnames like the query provided.
        '''
        sql_query = "SELECT * FROM Comic LEFT JOIN AltName ON Comic.id = AltName.comic_id " \
                    "WHERE Comic.name LIKE ? OR AltName.alt_name LIKE ?"
        response = cursor.execute(sql_query, (f"%{query}%", f"%{query}%"))

        comics = []
        for data in response.fetchall():
            comics.append(Comic(cursor, data['name'], data['cover_image_url'], data['status'],
                                data['description'], data['chapter_count'], data['rating'],
                                data['review_count'], data['date_added'], data['last_updated'],
                                data['year_published'], data['id']))

        return comics
    

    def get_reviews(self) -> list[Review]:
        """Gets all reviews associated with this Comic object.
        
        Accepts:
            * Just itself :)
        Returns:
            A list of reviews.
        """
        self.cursor.execute(
                "SELECT * FROM Review WHERE Review.comic_id = ?",
                (self.obj_id,)
            )

        reviews = []
        for review in self.cursor.fetchall():
            reviews.append(Review(self.cursor, self.obj_id, review['user_name'], review['rating'],
                                  review['review_text'], review['created_at'], review['updated_at'],
                                  review['id']))
            
        return reviews
    

    def get_comic_sources(self) -> list[ComicSource]:
        """Gets all comicsource objects associated to this comic in the database.
        
        Accepts:
            * Itself.
        Returns:
            A list of comicsource objects.
        """
        self.cursor.execute("SELECT * FROM Comic_Source WHERE Comic_Source.comic_id = ?", 
                            (self.obj_id, ))
        
        comic_sources = []
        for comic_source in self.cursor.fetchall():
            comic_sources.append(ComicSource(self.cursor, self.obj_id, comic_source['source_id'], 
                                             comic_source['chapter_count'], comic_source['status'],
                                             comic_source['slug'], comic_source['date_added'],
                                             comic_source['last_updated'], comic_source['id']))
            
        return comic_sources


    def create(self):
        self.cursor.execute(
                "INSERT INTO Comic (name, cover_image_url, status, description," \
                "chapter_count, rating, review_count, date_added, last_updated, year_published) " \
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.name, self.cover_image_url, self.status, self.description,
                self.chapter_count, self.rating, self.review_count, self.date_added,
                self.last_updated, self.year_published)
            )
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute("UPDATE Comic SET name = ?, cover_image_url = ?, status = ?," \
                            " description = ?," \
                            "chapter_count = ?, rating = ?, review_count = ?, date_added = ?, " \
                            "last_updated = ?, year_published = ? WHERE id = ?",
                            (self.name, self.cover_image_url, self.status, self.description,
                            self.chapter_count, self.rating, self.review_count, self.date_added,
                            self.last_updated, self.year_published, self.obj_id))


    def delete(self):
        self.cursor.execute("DELETE FROM Comic where id = ?",
                            (self.obj_id,))
