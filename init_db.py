from sqlite3orm import SQLite3ORM
db = SQLite3ORM("ytdownloads.db")

# db.drop_table("downloads") 
db.create_table("downloads", {"id": "INTEGER PRIMARY KEY", 
                              "url": "TEXT", 
                              "title": "TEXT",
                              "duration": "INTEGER",
                              "views": "INTEGER",
                              "filesize": "INTEGER",
                              "downloaded_at": "DATETIME"})