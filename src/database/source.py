"""Module used for interacting with or accessing with the Source table"""

from sqlite3 import Cursor

from src.database.database_row import DatabaseRow

class Source(DatabaseRow):
    """Represents a Genre record from the database.
    
    Special methods:
        get_all(cursor: Cursor) -> list[Source]
        Method used to gather all sources. Especially handy when running specific jobs.
    """
    def __init__(self, cursor: Cursor, name: str, base_url: str, 
                class_name: str, obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.name = name
        self.base_url = base_url
        self.class_name = class_name


    @staticmethod
    def get(cursor: Cursor, obj_id: int = None, name: str = None) -> Source | None:
        if obj_id is None and name is None:
            raise Exception("Both name and id cannot be None!")
        
        if obj_id is not None:
            query = f"SELECT * FROM Source WHERE id = ?"
            cursor.execute(query, (obj_id,))
        else:
            query = f"SELECT * FROM Source WHERE name = ?"
            cursor.execute(query, (name,))

        row = cursor.fetchone()
        if not row:
            return None

        return Source(cursor, row['name'], row['base_url'], row['class_name'], row['id'])
    

    @staticmethod
    def get_all(cursor: Cursor) -> list[Source]:
        query = f"SELECT * FROM Source"
        response = cursor.execute(query)

        sources = []
        for s in response.fetchall():
            source = Source(cursor, s['name'], s['base_url'], s['class_name'], s['id'])
            sources.append(source)

        return sources


    def create(self):
        self.cursor.execute(f"INSERT INTO Source (name, base_url, class_name) VALUES (?, ?, ?)",
                            (self.name, self.base_url, self.class_name))
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute("UPDATE Source SET name = ?, base_url = ?, class_name = ? WHERE id = ?",
                            (self.name, self.base_url, self.self.class_name, self.obj_id))
    

    def delete(self):
        self.cursor.execute("DELETE FROM Source WHERE id = ?",
                            (self.obj_id,))