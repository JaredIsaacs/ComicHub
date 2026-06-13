"""Module used for interacting with or accessing with the Review table."""


from sqlite3 import Cursor

from src.database.database_row import DatabaseRow

class Review(DatabaseRow):
    """Represents a Review record from the database."""
    def __init__(self, cursor: Cursor, comic_id: int, user_name: str, rating: float,
                review_text: str, created_at: str, updated_at: str, obj_id: int | None = None):
        super().__init__(cursor, obj_id)

        self.comic_id = comic_id
        self.user_name = user_name
        self.rating = rating
        self.review_text = review_text
        self.created_at = created_at
        self.updated_at = updated_at


    @staticmethod
    def get(cursor: Cursor, obj_id: int) -> Review | None:
        query = f"SELECT * FROM Review WHERE id = ?"
        cursor.execute(query, (obj_id,))

        row = cursor.fetchone()
        if not row:
            return None

        return Review(cursor, row['comic_id'], row['user_name'], row['rating'],
                    row['review_text'], row['created_at'], row['updated_at'], row['id'])


    def create(self):
        self.cursor.execute(
                "INSERT INTO Review (comic_id, user_name, rating, review_text, " \
                "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (self.comic_id, self.user_name, self.rating, 
                self.review_text, self.created_at, self.updated_at)
            )
        self.obj_id = self.cursor.lastrowid


    def update(self):
        self.cursor.execute(
                "UPDATE Review SET comic_id = ?, user_name = ?, rating = ?, " \
                "review_text = ?, created_at = ?, updated_at = ? WHERE id = ?",
                (self.comic_id, self.user_name, self.rating, 
                self.review_text, self.created_at, self.updated_at, self.obj_id)
            )


    def delete(self):
        self.cursor.execute(
                "DELETE FROM Review WHERE id = ?",
                (self.obj_id,)
            )
