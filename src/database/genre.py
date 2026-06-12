from src.database.database_row import DatabaseRow

from sqlite3 import Cursor

class Genre(DatabaseRow):
    def __init__(self, cursor: Cursor, name: str, genre_group: str, id: int | None = None):
        super().__init__(cursor, id)

        self.name = name
        self.genre_group = genre_group


    def associate_comic(self, comic_id: int):
        self.cursor.execute(
                "INSERT INTO Comic_Genre (comic_id, genre_id) VALUES (?, ?)",
                (comic_id, self.id))


    @staticmethod
    def get(cursor: Cursor, id: int| None = None, name: str| None = None) -> Genre | None:
        if not id and not name:
            raise ValueError('Either id or name must be provided')

        if id:
            cursor.execute('SELECT * FROM Genre WHERE id = ?', (id,))
        else:
            cursor.execute('SELECT * FROM Genre WHERE name = ?', (name,))

        row = cursor.fetchone()
        if not row:
            return None

        return Genre(cursor, row['name'], row['genre_group'], row['id'])
    

    def create(self):
        if self.id:
            create_query = 'INSERT INTO Genre (id, name, genre_group) VALUES (?, ?, ?)'
            self.cursor.execute(create_query, (self.id, self.name, self.genre_group))
        else:
            create_query = 'INSERT INTO Genre (name, genre_group) VALUES (?, ?)'
            self.cursor.execute(create_query, (self.name, self.genre_group))

        self.id = self.cursor.lastrowid

    def update(self):
        self.cursor.execute('UPDATE Genre SET name = ?, genre_group = ? WHERE id = ?', (self.name, self.genre_group, self.id))

    
    def delete(self):
        self.cursor.execute('DELETE FROM Genre WHERE id = ?', (self.id,))