import sqlite3
from datetime import datetime, timedelta

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

# Nettoyage des données trop vieilles
limite = datetime.now() - timedelta(days=30)
limite_str = limite.isoformat()
conn.execute("DELETE FROM metrics WHERE timestamp < ?", (limite_str,))

conn.commit()

rows = conn.execute("SELECT * FROM metrics").fetchall()
for row in rows:
    print(row)

conn.close()
