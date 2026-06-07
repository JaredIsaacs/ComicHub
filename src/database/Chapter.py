from src.database.DatabaseRow import DatabaseRow

from sqlite3 import Cursor

class Chapter(DatabaseRow):
    def __init__(self, cursor: Cursor, comic_source_id: int, chapter_number: float, id: int | None):
        super().__init__(cursor, id)

        self.id = id
        self.comic_source_id = comic_source_id
        self.chapter_number = chapter_number    


    @staticmethod
    def get(cursor: Cursor, id: int) -> 'Chapter':
        cursor.execute('SELECT * FROM chapters WHERE id = ?', (id,))
        row = cursor.fetchone()

        return Chapter(cursor, row[1], row[2], row[0])
    

    def create(self):
        self.cursor.execute('INSERT INTO chapters (comic_source_id, chapter_number) VALUES (?, ?)',
                             (self.comic_source_id, self.chapter_number))
        self.id = self.cursor.lastrowid

    
    def update(self):
        self.cursor.execute('UPDATE chapters SET comic_source_id = ?, chapter_number = ? WHERE id = ?',
                             (self.comic_source_id, self.chapter_number, self.id))

    def delete(self):
        self.cursor.execute('DELETE FROM chapters WHERE id = ?', (self.id,))