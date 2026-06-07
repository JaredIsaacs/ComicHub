from sqlite3 import Cursor

from src.database.DatabaseRow import DatabaseRow


class Review(DatabaseRow):
    def __init__(self, cursor: Cursor, comic_id: int, user_name: str, rating: float, review_text: str, id = None):
        super().__init__(cursor, id)

        self.comic_id = comic_id
        self.user_name = user_name
        self.rating = rating
        self.review_text = review_text

    
    @staticmethod
    def get(cursor: Cursor, id: int) -> Review:
        query = f"SELECT * FROM Review WHERE id = ?"
        response = cursor.execute(query, (id,))
        data = response.fetchone()

        return Review(cursor, data['comic_id'], data['user_name'], data['rating'], data['review_text'], data['id'])
    

    def create(self):
        self.cursor.execute(
                "INSERT INTO Review (comic_id, user_name, rating, review_text) VALUES (?, ?, ?, ?)",
                (self.comic_id, self.user_name, self.rating, self.review_text)
            )
        

    def update(self):
        self.cursor.execute(
                "UPDATE Review SET comic_id = ?, user_name = ?, rating = ?, review_text = ? WHERE id = ?",
                (self.comic_id, self.user_name, self.rating, self.review_text, self.id)
            )
        
    
    def delete(self):
        self.cursor.execute(
                "DELETE FROM Review WHERE id = ?",
                (self.id,)
            )