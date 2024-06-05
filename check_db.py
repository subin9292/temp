import sqlite3

def check_database():
    conn = sqlite3.connect('weather_grid.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM weather_grid LIMIT 5')
    rows = cur.fetchall()
    for row in rows:
        print(row)
    
    conn.close()

check_database()
