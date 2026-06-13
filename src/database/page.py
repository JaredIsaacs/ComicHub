"""Module used for interacting with or accessing with the Page table."""

from src.database.database_row import DatabaseRow

from sqlite3 import Cursor

class Page(DatabaseRow):
    """Represents a Page object from the database.

    Chapters are typically made up of multiple pages.
    """
    def __init__(self, cursor: Cursor, chapter_id: int, order: int, page_url: str, obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.chapter_id = chapter_id
        self.order = order
        self.page_url = page_url


    @staticmethod
    def get(cursor: Cursor, obj_id: int) -> Page | None:
        if not obj_id:
            raise Exception('ID must be provided')

        cursor.execute('SELECT * FROM Pages WHERE id = ?', (obj_id,))
        row = cursor.fetchone()
        if not row:
            return None

        return Page(cursor, row['chapter_id'], row['order'], row['page_url'], row['id'])


    def create(self):
        self.cursor.execute('INSERT INTO Pages (chapter_id, order, page_url) VALUES (?, ?, ?)', (self.chapter_id, self.order, self.page_url))
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute('UPDATE Pages SET chapter_id = ?, order = ?, page_url = ? WHERE id = ?', (self.chapter_id, self.order, self.page_url, self.obj_id))


    def delete(self):
        self.cursor.execute('DELETE FROM Pages WHERE id = ?', (self.obj_id,))
