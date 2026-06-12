from src.database.DatabaseRow import DatabaseRow

from sqlite3 import Cursor

class Comment(DatabaseRow):
    def __init__(self, cursor: Cursor, chapter_id: int, user_name: str, comment: str, id: int | None = None):
        super().__init__(cursor, id)

        self.chapter_id = chapter_id
        self.user_name = user_name
        self.comment = comment

    
    @staticmethod
    def get(cursor: Cursor, id: int) -> Comment | None:
        if not id:
            raise Exception('ID must be provided')

        query = f"SELECT * FROM Comment WHERE id = ?"
        cursor.execute(query, (id,))
        
        row = cursor.fetchone()
        if not row:
            return None

        return Comment(cursor, row['chapter_id'], row['user_name'], row['comment'], row['id'])
    

    def create(self):
        self.cursor.execute(
                "INSERT INTO Comment (chapter_id, user_name, comment) VALUES (?, ?, ?)",
                (self.chapter_id, self.user_name, self.comment)
            )
        self.id = self.cursor.lastrowid
        

    def update(self):
        self.cursor.execute(
                "UPDATE Comment SET chapter_id = ?, user_name = ?, comment = ? WHERE id = ?",
                (self.chapter_id, self.user_name, self.comment, self.id)
            )
        
    
    def delete(self):
        self.cursor.execute(
                "DELETE FROM Comment WHERE id = ?",
                (self.id,)
            )