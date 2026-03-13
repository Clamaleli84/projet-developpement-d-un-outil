import sqlite3

conn = sqlite3.connect('metrics.db')

conn.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        sonde     TEXT,
        valeur    REAL,
        unite     TEXT,
        timestamp TEXT DEFAULT (datetime('now'))
    )
""")

conn.execute(
    "INSERT INTO metrics (sonde, valeur, unite) VALUES (?, ?, ?)",
    ("cpu", 42.5, "%")
)

conn.commit() 

# PUIS on lit
rows = conn.execute("SELECT * FROM metrics").fetchall()
    
for row in rows:
    print(row)

conn.close()  
