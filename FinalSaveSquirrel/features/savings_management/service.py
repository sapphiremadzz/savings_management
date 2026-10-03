from features.savings_management.model import Savings
from features.savings_management.repository import SavingsRepository

#this handle the business logic and validation
class SavingsService:
    def __init__(self, repository: SavingsRepository):
        self.repository = repository

    @staticmethod
    def validate_amount(amount: str | float) -> float:
        """
            Utility method to validate user input for monetary amounts.
            Raises ValueError if the input is empty, non-numeric, or <= 0.
                """
        #check if amount is empty
        if isinstance(amount, str) and (not amount or not amount.strip()):
            raise ValueError("Please enter an amount.")
        try:
            valid_amount = float(amount)
        except ValueError:
            raise ValueError("Amount must be a valid number.")

        #check if amount is not less than 0, or negative numbers
        if valid_amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        return valid_amount

    def add_transaction(self, savings: Savings) -> Savings:
        """Validates amount input before requesting the repository to persist the new transaction."""
        savings.amount = self.validate_amount(savings.amount)
        return self.repository.add_transaction_list(savings)

    def get_transaction(self) -> list[Savings]:
        #fetch all transactions from the repository get_all_transactions()
        return self.repository.get_all_transactions()

    def delete(self, trans_id: int) -> Savings:
        """
        Constructs a minimal Savings entity using the target ID
        and delegates deletion to the repository.
        """
        delete_savings = Savings(
            id=trans_id,
            trans_type="Expense",
            category="General",
            amount=0.0,
            description="",
            date=""
        )
        return self.repository.delete_transaction(delete_savings)

    def fetch_formatted_history(self, limit: int | None = None) -> list[Savings]:
        """
        Retrieves transactions, trims the list if a limit is specified (e.g. top 20 for recent transaction dashboard),
        and returns clean Savings instances ready for display on the UI.
                """
        all_transactions = self.get_transaction()
        # Slice list if limit parameter is provided, if none keep full list
        history_items = all_transactions[:limit] if limit else all_transactions

        history_data = []
        for item in history_items:
            savings_obj = Savings(
                id=item.id,
                category=item.category ,
                description=(item.description or "").strip(),
                date=item.date or "",
                amount=item.amount,
                trans_type=item.trans_type,
            )
            history_data.append(savings_obj)

        return history_data

    def update(self, savings: Savings) -> Savings:
        """Validates updated amount before requesting the repository to save changes to the DB."""
        savings.amount = self.validate_amount(savings.amount)
        return self.repository.update_transaction(savings)