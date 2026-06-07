from sqlite3 import Cursor

from src.database.DatabaseRow import DatabaseRow


class Tag(DatabaseRow):
    def __init__(self, cursor: Cursor, name: str, id : int | None):
        super().__init__(cursor, id)

        self.name = name


    @staticmethod
    def get(cursor: Cursor, id: int = None, name: str = None) -> Tag:
        if id is None and name is None:
            raise Exception("Both name and id cannot be None!")
        
        if id:
            query = f"SELECT * FROM Tag WHERE id = ?"
            response = cursor.execute(query, (id,))
        else:
            query = f"SELECT * FROM Tag WHERE name = ?"
            response = cursor.execute(query, (name,))

        data = response.fetchone()
        return Tag(cursor, data['name'], data['id'])
    

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