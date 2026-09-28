from features.savings_management.model import Savings
from features.savings_management.repository import SavingsRepository

class SavingsService:
    def __init__(self, repository: SavingsRepository):
        self.repository = repository

    @staticmethod
    def validate_amount(amount: str | float) -> float:
        if isinstance(amount, str) and (not amount or not amount.strip()):
            raise ValueError("Please enter an amount.")
        try:
            valid_amount = float(amount)
        except ValueError:
            raise ValueError("Amount must be a valid number.")

        if valid_amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        return valid_amount

    def add_transaction(self, savings: Savings) -> Savings:
        savings.amount = self.validate_amount(savings.amount)
        return self.repository.add_transaction_list(savings)

    def get_transaction(self) -> list[Savings]:
        return self.repository.get_all_transactions()

    def delete(self, trans_id: int) -> Savings:
        delete_savings = Savings(
            id=trans_id,
            trans_type="Expense",
            category="General",
            amount=0.0,
            description="",
            date=""
        )
        return self.repository.delete_transaction(delete_savings)

    def fetch_formatted_history(self, limit: int | None = None) -> list[dict]:
        all_transactions = self.get_transaction()
        history_items = all_transactions[:limit] if limit else all_transactions

        history_data = []
        for item in history_items:
            history_data.append({
                "id": item.id,
                "category": item.category or "General",
                "description": (item.description or "").strip(),
                "date": item.date or "",
                "amount": item.amount,
                "is_expense": (item.trans_type == "Expense")
            })
        return history_data

    def update(self, savings: Savings) -> Savings:
        savings.amount = self.validate_amount(savings.amount)
        return self.repository.update_transaction(savings)