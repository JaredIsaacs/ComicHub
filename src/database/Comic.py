from sqlite3 import Cursor
from datetime import datetime, UTC

from src.database.DatabaseRow import DatabaseRow


class Comic(DatabaseRow):
    def __init__(self, cursor: Cursor, name: str, cover_image_url: str, status: str,
                description: str, chapter_count: float, rating: float, review_count:int,
                date_added: datetime, last_updated: datetime, year_published: int,  id = None):
        super().__init__(cursor, id)

        self.name = name
        self.cover_image_url = cover_image_url
        self.status = status
        self.description = description
        self.chapter_count = chapter_count
        self.rating = rating
        self.review_count = review_count
        self.date_added = date_added
        self.last_updated = last_updated
        self.year_published = year_published

    
    @staticmethod
    def get(cursor: Cursor, id: int = None, name: str = None) -> Comic:
        if id is None and name is None:
            raise Exception("Both name and id cannot be None!")
        
        if id:
            query = f"SELECT * FROM Comic WHERE id = ?"
            response = cursor.execute(query, (id,))
        else:
            query = f"SELECT * FROM Comic WHERE name = ?"
            response = cursor.execute(query, (name,))

        data = response.fetchone()
        return Comic(cursor, data['name'], data['cover_image_url'], data['status'], data['description'], data['chapter_count'],
                     data['rating'], data['review_count'], data['date_added'], data['last_updated'], data['year_published'],
                     data['id'])
    

    def create(self):
        self.cursor.execute(
                "INSERT INTO Comic (name, cover_image_url, status, description," \
                "chapter_count, rating, review_count, date_added, last_updated, year_published) VALUES " \
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (self.name, self.cover_image_url, self.status, self.description,
                self.chapter_count, self.rating, self.review_count, self.date_added,
                self.last_updated, self.year_published)
            )
    

    def update(self):
        self.cursor.execute("UPDATE Comic SET name = ?, cover_image_url = ?, status = ?, description = ?," \
                            "chapter_count = ?, rating = ?, review_count = ?, date_added = ?, last_updated = ?," \
                            "year_published = ?",
                            (self.name, self.cover_image_url, self.status, self.description, self.chapter_count,
                            self.rating, self.review_count, self.date_added, self.last_updated, self.year_published))
    

    def delete(self):
        self.cursor.execute("DELETE FROM Comic where id = ?",
                            (self.id,))

if __name__ == "__main__":
    from src.globals import DB_NAME
    import sqlite3

    now = datetime.now(UTC)
    now_iso = now.isoformat()

    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row

    cursor = con.cursor()

    comic = Comic.get(cursor, id=1)
    comic.delete()

    con.commit()
    con.close()