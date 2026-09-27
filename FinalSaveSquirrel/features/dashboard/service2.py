from features.savings_management.repository import SavingsRepository
from features.dashboard.model2 import SavingsDashboard

class DashboardService:
    def __init__(self, repository: SavingsRepository):
        self.repository = repository

    def calculate_savings(self):
        all_transactions = self.repository.get_all_transactions()

        income = sum(t.amount for t in all_transactions if t.trans_type == "Income")
        expense = sum(t.amount for t in all_transactions if t.trans_type == "Expense")
        savings = income - expense

        return income, expense, savings

    def fetch_dashboard_summary(self) -> SavingsDashboard:
        income, expense, savings = self.calculate_savings()
        return SavingsDashboard(
            income=income,
            expense=expense,
            savings=savings
        )