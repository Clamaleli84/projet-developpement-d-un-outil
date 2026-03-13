import sqlite3
from datetime import datetime, timedelta

class StorageManager:

    def __init__(self):
        self.conn = sqlite3.connect('metrics.db')
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                sonde     TEXT,
                valeur    REAL,
                unite     TEXT,
                timestamp TEXT DEFAULT (datetime('now'))
            )
        """)
        self.conn.commit()

    def save(self, sonde, valeur, unite):
        self.conn.execute(
            "INSERT INTO metrics (sonde, valeur, unite) VALUES (?, ?, ?)",
            (sonde, valeur, unite)
        )
        self.conn.commit()

    def cleanup(self):
        limite = datetime.now() - timedelta(days=30)
        limite_str = limite.isoformat()
        self.conn.execute(
            "DELETE FROM metrics WHERE timestamp < ?",
            (limite_str,)
        )
        self.conn.commit()

    def get_latest(self):
        rows = self.conn.execute("SELECT * FROM metrics").fetchall()
        return rows


# Test
storage = StorageManager()
storage.save("cpu", 42.5, "%")
storage.cleanup()
storage.get_latest()
