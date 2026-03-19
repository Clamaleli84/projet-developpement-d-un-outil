import sqlite3
from datetime import datetime, timedelta

class StorageManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sonde TEXT,
            val REAL,
            unit TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def save(self, sonde, val, unit):
        query = "INSERT INTO metrics (sonde, val, unit) VALUES (?, ?, ?)"
        self.conn.execute(query, (sonde, val, unit))
        self.conn.commit()
        
    def exists(self, sonde):
        depuis = (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        row = self.conn.execute(
            "SELECT id FROM metrics WHERE sonde = ? AND timestamp > ?",
            (sonde, depuis)
            ).fetchone()
        return row is not None

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
            "SELECT valeur, timestamp FROM metrics WHERE sonde = ? ORDER BY timestamp ASC",(sonde,)).fetchall()
        return rows
    
    def get_latest(self):
        rows = self.conn.execute("SELECT * FROM metrics").fetchall()
        return rows
