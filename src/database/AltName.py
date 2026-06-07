from sqlite3 import Cursor

from src.database.DatabaseRow import DatabaseRow


class AltName(DatabaseRow):
    def __init__(self, cursor: Cursor, comic_id: int, alt_name: str, id = None):
        super().__init__(cursor, id)

        self.comic_id = comic_id
        self.alt_name = alt_name

    
    @staticmethod
    def get(cursor: Cursor, id: int = None, comic_id: int = None) -> AltName:
        if id is None and comic_id is None:
            raise Exception("Both comic_id and id cannot be None!")
        
        if id:
            query = f"SELECT * FROM AltName WHERE id = ?"
            response = cursor.execute(query, (id,))
        else:
            query = f"SELECT * FROM AltName WHERE comic_id = ?"
            response = cursor.execute(query, (comic_id,))

        data = response.fetchone()
        return AltName(cursor, data['comic_id'], data['alt_name'], data['id'])
    

    def create(self):
        self.cursor.execute(
                "INSERT INTO AltName (comic_id, alt_name) VALUES (?, ?)", 
                (self.comic_id, self.alt_name)
            )
        
    
    def update(self):
        self.cursor.execute("UPDATE AltName SET comic_id = ?, alt_name = ?", (self.comic_id, self.alt_name))

    
    def delete(self):
        self.cursor.execute("DELETE FROM AltName WHERE id = ?", (self.id,))