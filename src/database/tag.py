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
    def __init__(self, cursor: Cursor, name: str, obj_id : int | None = None):
        super().__init__(cursor, obj_id)

        self.name = name


    def associate_comic(self, comic_id: int):
        """
        Links a tag to a comic.
        
        Accepts:
            * A comic id.

        Returns: 
            * Nothing.
        """

        self.cursor.execute(
                "INSERT INTO ComicTag (comic_id, tag_id) VALUES (?, ?)",
                (comic_id, self.obj_id))


    @staticmethod
    def get(cursor: Cursor, obj_id: int = None, name: str = None) -> Tag | None:
        if obj_id is None and name is None:
            raise ValueError("Both name and id cannot be None!")

        if obj_id is not None:
            query = "SELECT * FROM Tag WHERE id = ?"
            cursor.execute(query, (obj_id,))
        else:
            query = "SELECT * FROM Tag WHERE name = ?"
            cursor.execute(query, (name,))

        row = cursor.fetchone()
        if not row:
            return None

        return Tag(cursor, row['name'], row['id'])


    @staticmethod
    def get_all(cursor: Cursor) -> list[Tag]:
        """
        Grabs all tags that exists in the database

        Accepts:
            * cursor: Cursor

        Returns:
            * a list of tags (list[Tag])
        """

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
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute(
                "UPDATE Tag SET name = ? WHERE id = ?",
                (self.name, self.obj_id))


    def delete(self):
        self.cursor.execute(
                "DELETE FROM Tag WHERE id = ?",
                (self.obj_id,))
