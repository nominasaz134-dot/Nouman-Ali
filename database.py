import sqlite3

DB_NAME = "weather.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity INTEGER,
            weather TEXT,
            search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_weather(city, temp, humidity, weather):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO search_history
        (city, temperature, humidity, weather)
        VALUES (?, ?, ?, ?)
    """, (city, temp, humidity, weather))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city,
               temperature,
               humidity,
               weather,
               search_time
        FROM search_history
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows