from src.database.DatabaseRow import DatabaseRow

from sqlite3 import Cursor

class Chapter(DatabaseRow):
    def __init__(self, cursor: Cursor, comic_source_id: int, chapter_number: float, id: int | None = None):
        super().__init__(cursor, id)

        self.id = id
        self.comic_source_id = comic_source_id
        self.chapter_number = chapter_number    


    @staticmethod
    def get(cursor: Cursor, id: int) -> Chapter | None:
        cursor.execute('SELECT * FROM Chapters WHERE id = ?', (id,))

        row = cursor.fetchone()
        if not row:
            return None

        return Chapter(cursor, row['comic_source_id'], row['chapter_number'], row['id'])
    

    def create(self):
        self.cursor.execute('INSERT INTO Chapters (comic_source_id, chapter_number) VALUES (?, ?)',
                             (self.comic_source_id, self.chapter_number))
        self.id = self.cursor.lastrowid

    
    def update(self):
        self.cursor.execute('UPDATE Chapters SET comic_source_id = ?, chapter_number = ? WHERE id = ?',
                             (self.comic_source_id, self.chapter_number, self.id))

    def delete(self):
        self.cursor.execute('DELETE FROM Chapters WHERE id = ?', (self.id,))