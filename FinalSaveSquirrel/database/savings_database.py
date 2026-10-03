import sqlite3
from pathlib import Path

DB_NAME = "savings_management.db"

class SavingsDatabase:
    def __init__(self, database_path: str | Path = DB_NAME):
        #Initializes the database manager with a file path and automatically
        #ensures that required database tables exist on startup.

        self.database_path = Path(database_path)
        self.create_table()

    def connect(self) -> sqlite3.Connection:
        #Creates and returns a new SQLite connection context manager to execute SQL statements safely.
        return sqlite3.connect(self.database_path)

    def create_table(self) -> None:
        """
        Executes setup scripts to initialize the 'savings' and 'goals' tables
        if they do not already exist in the SQLite database file.
        """
        with self.connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS savings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    type TEXT NOT NULL,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL
                ); 

                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT NOT NULL, 
                    target_amount REAL NOT NULL, 
                    target_date TEXT NOT NULL
                );
            """)