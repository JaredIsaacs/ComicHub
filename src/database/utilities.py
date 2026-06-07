import sqlite3

from src.globals import DB_NAME

def initialize_database():
    '''Initializes the database as per the database_diagram.pdf schema'''

    con = sqlite3.connect(DB_NAME)
    cursor = con.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Comic (" \
                    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                    "name TEXT NOT NULL," \
                    "cover_image_url TEXT NOT NULL," \
                    "status TEXT NOT NULL DEFAULT 'N/A'," \
                    "description TEXT NOT NULL DEFAULT 'Not available.'," \
                    "chapter_count REAL NOT NULL DEFAULT 0.0," \
                    "rating REAL NOT NULL DEFAULT 0.0," \
                    "review_count INTEGER NOT NULL DEFAULT 0," \
                    "date_added TEXT NOT NULL," \
                    "last_updated TEXT NOT NULL," \
                    "year_published INTEGER DEFAULT 0"
                ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Source (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "name TEXT NOT NULL," \
                "base_url TEXT NOT NULL" \
            ");")

    cursor.execute("CREATE TABLE IF NOT EXISTS Comic_Source (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "comic_id INTEGER NOT NULL," \
                "source_id INTEGER NOT NULL," \
                "subscribed INTEGER DEFAULT 0," \
                "chapter_count REAL DEFAULT 0.0," \
                "status TEXT DEFAULT 'N/A'," \
                "slug TEXT NOT NULL," \
                "date_added TEXT NOT NULL," \
                "last_updated TEXT NOT NULL," \
                "FOREIGN KEY(comic_id) REFERENCES Comic(id)," \
                "FOREIGN KEY(source_id) REFERENCES Source(id)" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS AltName (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "comic_id INTEGER NOT NULL," \
                "alt_name TEXT NOT NULL," \
                "FOREIGN KEY(comic_ID) REFERENCES Comic(id) ON DELETE CASCADE" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Review (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "comic_id INTEGER NOT NULL," \
                "user_name TEXT DEFAULT 'N/A'," \
                "rating REAL DEFAULT 0.0," \
                "review_text TEXT NOT NULL," \
                "FOREIGN KEY(comic_ID) REFERENCES Comic(id) ON DELETE CASCADE" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Chapter (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "comic_source_id INTEGER NOT NULL," \
                "chapter_number REAL NOT NULL," \
                "FOREIGN KEY(comic_source_id) REFERENCES Comic_Source(id) ON DELETE CASCADE" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Page (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "chapter_id INTEGER NOT NULL," \
                "page_url TEXT NOT NULL," \
                "FOREIGN KEY(chapter_ID) REFERENCES Chapter(id) ON DELETE CASCADE" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Comment (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "chapter_id INTEGER NOT NULL," \
                "user_name TEXT DEFAULT 'N/A'," \
                "comment TEXT NOT NULL," \
                "FOREIGN KEY(chapter_id) REFERENCES Chapter(id) ON DELETE CASCADE" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Tag (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "name TEXT NOT NULL" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Genre (" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                "name TEXT NOT NULL" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Comic_Genre (" \
                "comic_id INTEGER NOT NULL," \
                "genre_id INTEGER NOT NULL," \
                "FOREIGN KEY(comic_id) REFERENCES Comic(id) ON DELETE CASCADE," \
                "FOREIGN KEY(genre_id) REFERENCES Genre(id) ON DELETE CASCADE" \
            ");")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS Comic_Tag (" \
                "comic_id INTEGER NOT NULL," \
                "tag_id INTEGER NOT NULL," \
                "FOREIGN KEY(comic_id) REFERENCES Comic(id) ON DELETE CASCADE," \
                "FOREIGN KEY(tag_id) REFERENCES Tag(id) ON DELETE CASCADE" \
            ");")


if __name__ == "__main__":
    initialize_database()