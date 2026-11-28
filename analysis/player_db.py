import sqlite3

DB_NAME = "players.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            team TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS swings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            score REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
