import sqlite3
from pathlib import Path

DB_NAME = "savings_management.db"

class SavingsDatabase:
    def __init__(self, database_path: str | Path = DB_NAME):
        self.database_path = Path(database_path)
        self.create_table()

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def create_table(self) -> None:
        with self.connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS savings (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                date TEXT NOT NULL)""")