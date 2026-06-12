from src.database.database_row import DatabaseRow

from sqlite3 import Cursor


class Page(DatabaseRow):
    def __init__(self, cursor: Cursor, chapter_id: int, order: int, page_url: str, id: int | None = None):
        super().__init__(cursor, id)

        self.chapter_id = chapter_id
        self.order = order  
        self.page_url = page_url


    @staticmethod
    def get(cursor: Cursor, id: int) -> Page | None:
        if not id:
            raise Exception('ID must be provided')

        cursor.execute('SELECT * FROM Pages WHERE id = ?', (id,))
        row = cursor.fetchone()
        if not row:
            return None

        return Page(cursor, row['chapter_id'], row['order'], row['page_url'], row['id'])


    def create(self):
        self.cursor.execute('INSERT INTO Pages (chapter_id, order, page_url) VALUES (?, ?, ?)', (self.chapter_id, self.order, self.page_url))
        self.id = self.cursor.lastrowid

    
    def update(self):
        self.cursor.execute('UPDATE Pages SET chapter_id = ?, order = ?, page_url = ? WHERE id = ?', (self.chapter_id, self.order, self.page_url, self.id))

    
    def delete(self):
        self.cursor.execute('DELETE FROM Pages WHERE id = ?', (self.id,))