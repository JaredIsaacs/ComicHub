"""Module used for interacting with or accessing with the Genre table."""

from sqlite3 import Cursor

from src.database.database_row import DatabaseRow

class Genre(DatabaseRow):
    """Represents a Genre record from the database.

    Special methods:
        associate_comic(self, comic_id: int):
        Is used to link a comic to a genre using a comic_id.

        This being on the genre might be temporary, as grabbing a group of genres then tagging them
        all at once on the comic object is probably waaay more efficient. But whatever, this works.
    """
    def __init__(self, cursor: Cursor, name: str, genre_group: str, obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.name = name
        self.genre_group = genre_group


    def associate_comic(self, comic_id: int):
        """
        Associates this specific genre to a comic.

        Accepts:
            * A comic ID

        Returns:
            * Nothing
        """
        self.cursor.execute(
                "INSERT INTO Comic_Genre (comic_id, genre_id) VALUES (?, ?)",
                (comic_id, self.obj_id))


    @staticmethod
    def get(cursor: Cursor, obj_id: int| None = None, name: str| None = None) -> Genre | None:
        if not id and not name:
            raise ValueError('Either id or name must be provided')

        if obj_id is not None:
            cursor.execute('SELECT * FROM Genre WHERE id = ?', (obj_id,))
        else:
            cursor.execute('SELECT * FROM Genre WHERE name = ?', (name,))

        row = cursor.fetchone()
        if not row:
            return None

        return Genre(cursor, row['name'], row['genre_group'], row['id'])


    def create(self):
        if self.obj_id:
            create_query = 'INSERT INTO Genre (id, name, genre_group) VALUES (?, ?, ?)'
            self.cursor.execute(create_query, (self.obj_id, self.name, self.genre_group))
        else:
            create_query = 'INSERT INTO Genre (name, genre_group) VALUES (?, ?)'
            self.cursor.execute(create_query, (self.name, self.genre_group))

            self.obj_id = self.cursor.lastrowid

    def update(self):
        self.cursor.execute('UPDATE Genre SET name = ?, genre_group = ? WHERE id = ?',
                            (self.name, self.genre_group, self.obj_id))


    def delete(self):
        self.cursor.execute('DELETE FROM Genre WHERE id = ?', (self.obj_id,))
