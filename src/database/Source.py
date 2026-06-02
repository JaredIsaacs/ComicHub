from sqlite3 import Cursor

from src.database.DatabaseRow import DatabaseRow

class Source(DatabaseRow):
    def __init__(self, cursor: Cursor, name: str, base_url: str, id: int | None = None):
        super().__init__(cursor, id)

        self.name = name
        self.base_url = base_url


    @staticmethod
    def get(cursor: Cursor, id = None, name = None):
        if id is None and name is None:
            raise Exception("Both name and id cannot be None!")
        
        if id:
            query = f"SELECT * FROM Source WHERE id = ?"
            response = cursor.execute(query, (id,))
        else:
            query = f"SELECT * FROM Source WHERE name = ?"
            response = cursor.execute(query, (name,))

        data = response.fetchone()
        return Source(cursor, data['name'], data['base_url'], data['id'])


    def create(self):
        self.cursor.execute(f"INSERT INTO Source (name, base_url) VALUES (?, ?)",
                            (self.name, self.base_url))


    def update(self):
        self.cursor.execute("UPDATE Source SET name = ?, base_url = ? WHERE id = ?",
                            (self.name, self.base_url, self.id))
    

    def delete(self):
        self.cursor.execute("DELETE FROM Source WHERE id = ?",
                            (self.id,))


if __name__ == "__main__":
    import sqlite3
    from src.globals import DB_NAME

    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row

    cursor = con.cursor()

    source = Source(cursor, name="Asura Scans", base_url="asurascans.com")
    source.create()

    con.commit()
    con.close()