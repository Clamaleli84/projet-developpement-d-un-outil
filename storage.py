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
        
    def exists(self, sonde):
        depuis = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        row = self.conn.execute(
            "SELECT id FROM metrics WHERE sonde = ? AND timestamp > ?",
            (sonde, depuis)
            ).fetchone()
        return row is not None
    
    def save(self, sonde, valeur, unite):
        if self.exists(sonde):
            print(f"⚠ {sonde} déjà enregistré récemment, on ignore.")
            return
        self.conn.execute("INSERT INTO metrics (sonde, valeur, unite) VALUES (?, ?, ?)",(sonde, valeur, unite))
        self.conn.commit()

    def cleanup(self):
        limite = datetime.now() - timedelta(days=30)
        limite_str = limite.isoformat()
        self.conn.execute(
            "DELETE FROM metrics WHERE timestamp < ?",
            (limite_str,)
        )
        self.conn.commit()

    def get_history(self, sonde):
    rows = self.conn.execute(
        "SELECT valeur, timestamp FROM metrics WHERE sonde = ? ORDER BY timestamp ASC",
        (sonde,)
    ).fetchall()
    return rows
    
    def get_latest(self):
        rows = self.conn.execute("SELECT * FROM metrics").fetchall()
        return rows
