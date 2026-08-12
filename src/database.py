import sqlite3
def init_database():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summary TEXT NOT NULL,
        intent TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
    conn.commit()
    conn.close()
def save_event(summary, intent, date, time):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO events(
            summary, intent, date, time)
            VALUES (?,?,?,?)""", (summary, intent, date, time))
    conn.commit()
    conn.close()
    
def get_events_date(date):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE date = ?" , (date,))
    results = cursor.fetchall()
    conn.close()
    return results
    