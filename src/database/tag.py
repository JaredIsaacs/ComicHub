"""Module used for interacting with or accessing with the Tag table."""

from sqlite3 import Cursor

from src.database.database_row import DatabaseRow


class Tag(DatabaseRow):
    """Represents a Genre record from the database.

    Special methods:
        get_all(cursor: Cursor) -> list[Tag]:
        Returns all tags available in the db. Might be handy when setting up filtering
        on the frontend.
    """
    def __init__(self, cursor: Cursor, name: str, id : int | None = None):
        super().__init__(cursor, id)

        self.name = name


    def associate_comic(self, comic_id: int):
        self.cursor.execute(
                "INSERT INTO ComicTag (comic_id, tag_id) VALUES (?, ?)",
                (comic_id, self.id))


    @staticmethod
    def get(cursor: Cursor, id: int = None, name: str = None) -> Tag | None:
        if id is None and name is None:
            raise Exception("Both name and id cannot be None!")

        if id:
            query = f"SELECT * FROM Tag WHERE id = ?"
            cursor.execute(query, (id,))
        else:
            query = f"SELECT * FROM Tag WHERE name = ?"
            cursor.execute(query, (name,))

        row = cursor.fetchone()
        if not row:
            return None

        return Tag(cursor, row['name'], row['id'])


    @staticmethod
    def get_all(cursor: Cursor) -> list[Tag]:
        query = "SELECT * FROM Tag"
        response = cursor.execute(query)

        tags = []
        for data in response.fetchall():
            tags.append(Tag(cursor, data['name'], data['id']))

        return tags


    def create(self):
        self.cursor.execute(
                "INSERT INTO Tag (name) VALUES (?)",
                (self.name,))
        self.id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute(
                "UPDATE Tag SET name = ? WHERE id = ?",
                (self.name, self.id))


    def delete(self):
        self.cursor.execute(
                "DELETE FROM Tag WHERE id = ?",
                (self.id,))
