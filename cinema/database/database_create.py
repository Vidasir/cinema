import sqlite3

db = sqlite3.connect('info.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
name TEXT,
surname TEXT,
patronymic TEXT,
passport INTEGER,
birth_date TEXT,
inn INTEGER,
city TEXT,
phone_number INTEGER
)
""")


sql.execute("""
CREATE TABLE IF NOT EXISTS films (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
film TEXT,
date TEXT
)
""")

sql.execute("""CREATE TABLE IF NOT EXISTS views (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
id_users INTEGER,
id_film INTEGER
)
""")

db.commit()