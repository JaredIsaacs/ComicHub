"""Module used for interacting with or accessing the Alt_Name table."""

from sqlite3 import Cursor

from src.database.database_row import DatabaseRow


class AltName(DatabaseRow):
    """Represents Alternative Names that a comic could potentially be called."""
    def __init__(self, cursor: Cursor, comic_id: int, alt_name: str, row_id: int | None = None):
        super().__init__(cursor, row_id)

        self.comic_id = comic_id
        self.alt_name = alt_name


    @staticmethod
    def get(cursor: Cursor, obj_id: int = None, comic_id: int = None) -> AltName | None:
        if obj_id is None and comic_id is None:
            raise ValueError("Both comic_id and id cannot be None!")

        if obj_id is not None:
            query = "SELECT * FROM AltName WHERE id = ?"
            cursor.execute(query, (id,))
        else:
            query = "SELECT * FROM AltName WHERE comic_id = ?"
            cursor.execute(query, (comic_id,))

        row = cursor.fetchone()
        if not row:
            return None

        return AltName(cursor, row['comic_id'], row['alt_name'], row['id'])


    def create(self):
        self.cursor.execute(
                "INSERT INTO AltName (comic_id, alt_name) VALUES (?, ?)",
                (self.comic_id, self.alt_name)
            )
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute("UPDATE AltName SET comic_id = ?, alt_name = ?",
                            (self.comic_id, self.alt_name))


    def delete(self):
        self.cursor.execute("DELETE FROM AltName WHERE id = ?", (self.obj_id,))
