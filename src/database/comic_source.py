"""Module used for interacting with or accessing with the Comic_Source table."""

from sqlite3 import Cursor

from src.database.database_row import DatabaseRow
from src.database.source import Source

class ComicSource(DatabaseRow):
    """Represents the connection between a Comic and a Source.

    Many to many relationship allows us to keep specific Comic + Source data
    together.

    Special methods:
        get_all_by_comic_id(cursor, comic_id: int) -> list[ComicSource]:
        Returns all Comic_Source records that relate to a specific Comic id.

        get_all_by_source_id(cursor, source_id: int) -> list[ComicSource]:
        Returns all Comic_Source records that relate to a specific Source id.

    """
    def __init__(self, cursor: Cursor, comic_id: int, source_id: int,
                chapter_count: float, status: str, slug: str,
                date_added: str, last_updated: str, obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.comic_id = comic_id
        self.source_id = source_id
        self.chapter_count = chapter_count
        self.status = status
        self.slug = slug
        self.date_added = date_added
        self.last_updated = last_updated


    @staticmethod
    def get(cursor, obj_id: int = None, comic_id: int = None,
            source_id: int = None) -> ComicSource | None:
        if obj_id is None and comic_id is None and source_id is None:
            raise ValueError("Either id or both comic_id and source_id must be provided!")

        if obj_id:
            query = "SELECT * FROM Comic_Source WHERE id = ?"
            cursor.execute(query, (obj_id,))
        else:
            query = "SELECT * FROM Comic_Source WHERE comic_id = ? AND source_id = ?"
            cursor.execute(query, (comic_id, source_id))

        row = cursor.fetchone()
        if not row:
            return None

        return ComicSource(cursor, row['comic_id'], row['source_id'], row['chapter_count'],
                            row['status'], row['slug'], row['date_added'], row['last_updated'],
                            row['id'])


    @staticmethod
    def get_all_by_comic_id(cursor, comic_id: int) -> list[ComicSource]:
        '''
        Accepts:
            * cursor: Cursor
            * comic_id: int

        Returns:
            A list of all Comic_Sources associated to a comic_id
        '''
        query = "SELECT * FROM Comic_Source WHERE comic_id = ?"
        response = cursor.execute(query, (comic_id,))
        data = response.fetchall()
        return [ComicSource(cursor, row['comic_id'], row['source_id'], row['chapter_count'],
                            row['status'], row['slug'], row['date_added'], row['last_updated'],
                            row['id']) for row in data]


    @staticmethod
    def get_all_by_source_id(cursor, source_id: int) -> list[ComicSource]:
        '''
        Accepts:
            * cursor: Cursor
            * source_id: int

        Returns:
            A list of all Comic_Sources associated to a source_id
        '''
        query = "SELECT * FROM Comic_Source WHERE source_id = ?"
        response = cursor.execute(query, (source_id,))
        data = response.fetchall()
        return [ComicSource(cursor, row['comic_id'], row['source_id'], row['chapter_count'],
                            row['status'], row['slug'], row['date_added'], row['last_updated'],
                            row['id']) for row in data]
    

    def get_source(self) -> Source:
        self.cursor.execute("SELECT * FROM Source where id = ?", (self.source_id,))
        source = self.cursor.fetchone()

        return Source(self.cursor, source['name'], source['base_url'], source['class_name'],
                      source['id'])


    def create(self):
        self.cursor.execute(
            "INSERT INTO Comic_Source (comic_id, source_id, chapter_count, status," \
            " slug, date_added, last_updated) " \
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (self.comic_id, self.source_id, self.chapter_count, self.status, self.slug,
            self.date_added, self.last_updated))
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute(
            "UPDATE Comic_Source SET comic_id = ?, source_id = ?, chapter_count = ?, status = ?, " \
            "slug = ?, date_added = ?, last_updated = ? " \
            "WHERE id = ?",
            (self.comic_id, self.source_id, self.chapter_count, self.status, self.slug,
            self.date_added, self.last_updated, self.obj_id))


    def delete(self):
        self.cursor.execute("DELETE FROM Comic_Source WHERE id = ?",
                            (self.obj_id,))
