from sqlite3 import Cursor
from datetime import datetime, UTC

from src.database.DatabaseRow import DatabaseRow


class Comic(DatabaseRow):
    def __init__(self, cursor: Cursor, name: str, cover_image_url: str, status: str,
                description: str, chapter_count: float, rating: float, review_count:int,
                date_added: datetime, last_updated: datetime, year_published: int,  id : int | None):
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
    

    @staticmethod
    def search(cursor: Cursor, query: str) -> list[Comic]:
        sql_query = f"SELECT * FROM Comic, LEFT JOIN AltName ON Comic.id = AltName.comic_id" \
                    f"WHERE Comic.name LIKE ? OR AltName.alt_name LIKE ?"
        response = cursor.execute(sql_query, (f"%{query}%", f"%{query}%"))

        comics = []
        for data in response.fetchall():
            comics.append(Comic(cursor, data['name'], data['cover_image_url'], data['status'], data['description'], data['chapter_count'],
                                data['rating'], data['review_count'], data['date_added'], data['last_updated'], data['year_published'],
                                data['id']))
        
        return comics


    def create(self):
        self.cursor.execute(
                "INSERT INTO Comic (name, cover_image_url, status, description," \
                "chapter_count, rating, review_count, date_added, last_updated, year_published) VALUES " \
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (self.name, self.cover_image_url, self.status, self.description,
                self.chapter_count, self.rating, self.review_count, self.date_added,
                self.last_updated, self.year_published)
            )
        self.id = self.cursor.lastrowid
    

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

    comic = Comic(cursor, "Dragonslayer's Class Regression", "https://meo.comick.pictures/Z8Bb6v-s.jpg", "ongoing", "Zeke Draker was the first of House Draker to fail his Awakening. And for that, he was cast out. Forced to survive in a brutal world, Zeke rose from disgrace and earned the name Phantom of the North. On a mission to stop the emperor from obtaining an ancient relic, Zeke was hunted and killed by imperial forces. But fate had other plans. Zeke awakens as a 12-year-old boy back in the Cradle, House Draker’s elite training ground. Given a second chance, Zeke’s determined to rewrite his fate.", 87.0, 7.9, 1440, now_iso, now_iso, 2024)
    comic.create()

    con.commit()
    con.close()