from datetime import UTC, datetime
from sqlite3 import Cursor

from src.database.DatabaseRow import DatabaseRow

class ComicSource(DatabaseRow):
    def __init__(self, cursor: Cursor, comic_id: int, source_id: int, 
                 chapter_count: float, status: str, slug: str,
                 date_added: str, last_updated: str, id: int | None = None):
        super().__init__(cursor, id)

        self.comic_id = comic_id
        self.source_id = source_id
        self.chapter_count = chapter_count
        self.status = status
        self.slug = slug
        self.date_added = date_added
        self.last_updated = last_updated

    
    @staticmethod
    def get(cursor, id: int = None, comic_id: int = None, source_id: int = None) -> ComicSource:
        if id is None and comic_id is None and source_id is None:
            raise Exception("Either id or both comic_id and source_id must be provided!")
        
        if id:
            query = "SELECT * FROM Comic_Source WHERE id = ?"
            response = cursor.execute(query, (id,))
        else:
            query = "SELECT * FROM Comic_Source WHERE comic_id = ? AND source_id = ?"
            response = cursor.execute(query, (comic_id, source_id))

        data = response.fetchone()
        return ComicSource(cursor, data['comic_id'], data['source_id'], data['chapter_count'], data['status'],
                           data['slug'], data['date_added'], data['last_updated'], data['id'])
    
    
    @staticmethod
    def get_all_by_comic_id(cursor, comic_id: int) -> list[ComicSource]:
        query = "SELECT * FROM Comic_Source WHERE comic_id = ?"
        response = cursor.execute(query, (comic_id,))
        data = response.fetchall()
        return [ComicSource(cursor, row['comic_id'], row['source_id'], row['chapter_count'], row['status'],
                            row['slug'], row['date_added'], row['last_updated'], row['id']) for row in data]


    @staticmethod
    def get_all_by_source_id(cursor, source_id: int) -> list[ComicSource]:
        query = "SELECT * FROM Comic_Source WHERE source_id = ?"
        response = cursor.execute(query, (source_id,))
        data = response.fetchall()
        return [ComicSource(cursor, row['comic_id'], row['source_id'], row['chapter_count'], row['status'],
                            row['slug'], row['date_added'], row['last_updated'], row['id']) for row in data]


    def create(self):
        self.cursor.execute(
            "INSERT INTO Comic_Source (comic_id, source_id, chapter_count, status, slug, date_added, last_updated) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (self.comic_id, self.source_id, self.chapter_count, self.status, self.slug,
             self.date_added, self.last_updated))
        self.id = self.cursor.lastrowid
    

    def update(self):
        self.cursor.execute(
            "UPDATE Comic_Source SET comic_id = ?, source_id = ?, chapter_count = ?, status = ?, slug = ?, date_added = ?, last_updated = ? "
            "WHERE id = ?",
            (self.comic_id, self.source_id, self.chapter_count, self.status, self.slug,
             self.date_added, self.last_updated, self.id))
    

    def delete(self):
        self.cursor.execute("DELETE FROM Comic_Source WHERE id = ?",
                            (self.id,))
    

if __name__ == "__main__":
    import sqlite3
    from src.globals import DB_NAME

    now = datetime.now(UTC)
    now_iso = now.isoformat()

    con = sqlite3.connect(DB_NAME)
    con.row_factory = sqlite3.Row

    cursor = con.cursor()

    commic_source = ComicSource(cursor, comic_id=2, source_id=1, chapter_count=87.0, status="Ongoing", slug="a-dragonslayers-peerless-regression-7b57f74d", date_added=now_iso, last_updated=now_iso)
    commic_source.create()

    con.commit()
    con.close()