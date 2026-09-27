from database.savings_database import SavingsDatabase
from features.savings_management.model import Savings

class SavingsRepository:
    def __init__(self, database: SavingsDatabase):
        self.database = database

    def add_transaction_list(self, savings: Savings) -> Savings:
        with self.database.connect() as conn:
            cursor = conn.execute("""
                INSERT INTO savings (type, category, amount, description, date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                savings.trans_type,
                savings.category,
                savings.amount,
                savings.description,
                savings.date
            ))
            savings.id = cursor.lastrowid
        return savings

    def get_all_transactions(self) -> list[Savings]:
        with self.database.connect() as conn:
            rows = conn.execute(
                "SELECT id, type, category, amount, description, date FROM savings ORDER BY id DESC"
            ).fetchall()
        return [Savings(
            id=row[0],
            trans_type=row[1],
            category=row[2],
            amount=row[3],
            description=row[4],
            date=row[5]
        ) for row in rows]

    def delete_transaction(self, savings: Savings) -> Savings:
        with self.database.connect() as conn:
            conn.execute("DELETE FROM savings WHERE id = ?", (savings.id,))
        return savings

    def update_transaction(self, savings: Savings) -> Savings:
        with self.database.connect() as conn:
            conn.execute("""
                UPDATE savings
                SET type = ?, category = ?, amount = ?, description = ?, date = ?
                WHERE id = ?
            """, (
                savings.trans_type,
                savings.category,
                savings.amount,
                savings.description,
                savings.date,
                savings.id
            ))
        return savings