from features.savings_management.repository import SavingsRepository
from features.dashboard.model2 import Dashboard

class DashboardService:
    def __init__(self, repository: SavingsRepository):
        self.repository = repository

    def calculate_savings(self) -> tuple[float, float, float]:
        """
        Retrieves all transaction history from the repository and computes:
        1. Total Income
        2. Total Expense
        3. Net Savings (Income - Expense)
        """
        # Fetch all saved transaction entries from DB
        all_transactions = self.repository.get_all_transactions()
        # Sum amounts matching transaction type "Income"
        income = sum(t.amount for t in all_transactions if t.trans_type == "Income")
        # Sum amounts matching transaction type "Expense"
        expense = sum(t.amount for t in all_transactions if t.trans_type == "Expense")
        # Calculate net savings
        savings = income - expense
        return income, expense, savings

    def fetch_dashboard_summary(self) -> Dashboard:
        income, expense, savings = self.calculate_savings()
        return Dashboard(
            income=income,
            expense=expense,
            savings=savings
        )