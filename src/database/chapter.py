"""Module used for interacting with or accessing with the Chapter table."""

from src.database.database_row import DatabaseRow

from sqlite3 import Cursor

class Chapter(DatabaseRow):
    """Represents Chapters that a comic source has."""
    def __init__(self, cursor: Cursor, comic_source_id: int, chapter_number: float, obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.comic_source_id = comic_source_id
        self.chapter_number = chapter_number


    @staticmethod
    def get(cursor: Cursor, obj_id: int) -> Chapter | None:
        cursor.execute('SELECT * FROM Chapters WHERE id = ?', (obj_id,))

        row = cursor.fetchone()
        if not row:
            return None

        return Chapter(cursor, row['comic_source_id'], row['chapter_number'], row['id'])


    def create(self):
        self.cursor.execute("INSERT INTO Chapters (comic_source_id, chapter_number) VALUES (?, ?)",
                            (self.comic_source_id, self.chapter_number))
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute("UPDATE Chapters SET comic_source_id = ?, chapter_number = ? " \
                            "WHERE id = ?",
                            (self.comic_source_id, self.chapter_number, self.obj_id))

    def delete(self):
        self.cursor.execute("DELETE FROM Chapters WHERE id = ?", (self.obj_id,))
