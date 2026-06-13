"""Module used for interacting with or accessing with the Comic table."""

from sqlite3 import Cursor
from datetime import datetime, UTC

from src.database.database_row import DatabaseRow


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
                date_added: datetime, last_updated: datetime, year_published: int,  obj_id : int | None = None):
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
            raise Exception("Both name and id cannot be None!")

        if obj_id is not None:
            query = f"SELECT * FROM Comic WHERE id = ?"
            cursor.execute(query, (obj_id,))
        else:
            query = f"SELECT * FROM Comic LEFT JOIN AltName ON Comic.id = AltName.comic_id " \
            "WHERE Comic.name = ? OR AltName.alt_name = ?"
            cursor.execute(query, (name, name))

        row = cursor.fetchone()
        if not row:
            return None

        return Comic(cursor, row['name'], row['cover_image_url'], row['status'], row['description'],
                     row['chapter_count'], row['rating'], row['review_count'], row['date_added'],
                     row['last_updated'], row['year_published'], row['id'])


    @staticmethod
    def search(cursor: Cursor, query: str) -> list[Comic]:
        sql_query = f"SELECT * FROM Comic LEFT JOIN AltName ON Comic.id = AltName.comic_id " \
                    f"WHERE Comic.name LIKE ? OR AltName.alt_name LIKE ?"
        response = cursor.execute(sql_query, (f"%{query}%", f"%{query}%"))

        comics = []
        for data in response.fetchall():
            comics.append(Comic(cursor, data['name'], data['cover_image_url'], data['status'],
                                data['description'], data['chapter_count'], data['rating'],
                                data['review_count'], data['date_added'], data['last_updated'],
                                data['year_published'], data['id']))

        return comics


    def create(self):
        self.cursor.execute(
                "INSERT INTO Comic (name, cover_image_url, status, description," \
                "chapter_count, rating, review_count, date_added, last_updated, year_published) VALUES " \
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.name, self.cover_image_url, self.status, self.description,
                self.chapter_count, self.rating, self.review_count, self.date_added,
                self.last_updated, self.year_published)
            )
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute("UPDATE Comic SET name = ?, cover_image_url = ?, status = ?, description = ?," \
                            "chapter_count = ?, rating = ?, review_count = ?, date_added = ?, last_updated = ?," \
                            "year_published = ?",
                            (self.name, self.cover_image_url, self.status, self.description, self.chapter_count,
                            self.rating, self.review_count, self.date_added, self.last_updated, self.year_published))


    def delete(self):
        self.cursor.execute("DELETE FROM Comic where id = ?",
                            (self.obj_id,))
