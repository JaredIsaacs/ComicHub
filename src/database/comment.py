"""Module used for interacting with or accessing with the Comment table."""

from sqlite3 import Cursor

from src.database.database_row import DatabaseRow

class Comment(DatabaseRow):
    """Represents the and individual Comment row from the database."""
    def __init__(self, cursor: Cursor, chapter_id: int, user_name: str, comment: str,
                obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.chapter_id = chapter_id
        self.user_name = user_name
        self.comment = comment


    @staticmethod
    def get(cursor: Cursor, obj_id: int) -> Comment | None:
        if not obj_id:
            raise ValueError('id must be provided')

        query = "SELECT * FROM Comment WHERE id = ?"
        cursor.execute(query, (obj_id,))

        row = cursor.fetchone()
        if not row:
            return None

        return Comment(cursor, row['chapter_id'], row['user_name'], row['comment'], row['id'])


    def create(self):
        self.cursor.execute(
                "INSERT INTO Comment (chapter_id, user_name, comment) VALUES (?, ?, ?)",
                (self.chapter_id, self.user_name, self.comment)
            )
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute(
                "UPDATE Comment SET chapter_id = ?, user_name = ?, comment = ? WHERE id = ?",
                (self.chapter_id, self.user_name, self.comment, self.obj_id)
            )


    def delete(self):
        self.cursor.execute(
                "DELETE FROM Comment WHERE id = ?",
                (self.obj_id,)
            )
