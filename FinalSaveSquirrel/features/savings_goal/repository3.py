from features.savings_goal.model3 import Goal
from database.savings_database import SavingsDatabase

class GoalRepository:
    def __init__(self, database: SavingsDatabase):
        self.database = database

    def add_goal(self, goals: Goal) -> Goal:
        """Inserts a new Goal record into the database table 'goals'."""
        with self.database.connect() as conn:
            cursor = conn.execute("""
                   INSERT INTO goals (title, target_amount, target_date)
                   VALUES (?, ?, ?)
               """, (
                goals.title,
                goals.target_amount,
                goals.target_date
            ))
            goals.id = cursor.lastrowid
        return goals

    def get_all_goals(self) -> list[Goal]:
        """Retrieves all active goals ordered by ID descending (newest first)."""
        with self.database.connect() as conn:
            rows = conn.execute("SELECT id, "
                                "title, "
                                "target_amount, "
                                "target_date "
                                "FROM goals ORDER BY id DESC").fetchall()
            return [Goal(id=row[0],
                         title=row[1],
                         target_amount=row[2],
                         target_date=row[3])
                    for row in rows]

    def delete_goal(self, goals: Goal) -> Goal:
        """Deletes a goal from database matching the given goal ID."""
        with self.database.connect() as conn:
            conn.execute("DELETE FROM goals WHERE id = ?", (goals.id,))
        return goals