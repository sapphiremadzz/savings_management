from datetime import datetime, date
from features.savings_goal.repository3 import GoalRepository
from features.dashboard.service2 import DashboardService
from features.savings_goal.model3 import Goal
from features.savings_management.service import SavingsService  # Import validation logic[cite: 6]

class ServiceGoal:
    def __init__(self, repository: GoalRepository, dashboard_service: DashboardService):
        """Injects GoalRepository and DashboardService dependencies."""
        self.repository = repository
        self.dashboard_service = dashboard_service

    def add_goal(self, goal: Goal) -> Goal:
        """Validates target amount before inserting goal into DB."""
        goal.target_amount = SavingsService.validate_amount(goal.target_amount)
        return self.repository.add_goal(goal)

    def get_goals(self) -> list[Goal]:
        #fetches all saving goals
        return self.repository.get_all_goals()

    def delete_goals(self, trans_id: int) -> Goal:
        delete_goals = Goal(
            id=trans_id,
            title="Deleting Goal",
            target_amount=1.0,
            target_date="2000-01-01"
        )
        return self.repository.delete_goal(delete_goals)

    def get_remaining_days_text(self, target_date_input: str | date) -> str:
        today = date.today() #set the date today

        # Convert string date ('YYYY-MM-DD') into a Python date object
        if isinstance(target_date_input, str):
            if not target_date_input.strip():
                return "No target date set"
            target_dt = datetime.strptime(
                target_date_input, "%Y-%m-%d"
            ).date()
        else:
            target_dt = target_date_input

        #this is for computing date differences
        remaining_days = (target_dt - today).days

        if remaining_days > 0:
            return f"You have {remaining_days} days remaining"
        elif remaining_days == 0:
            return "Target date is today"
        else:
            return f"Overdue by {abs(remaining_days)} days"

    def get_current_savings(self)-> float:
        """Retrieves user's total net savings calculated from DashboardService."""
        current_savings = self.dashboard_service.fetch_dashboard_summary()
        return current_savings.get_savings()

    def needed_amount(self, goal: Goal) -> float:
        """
        Calculates remaining amount required to achieve the target goal.
        Returns 0.00 if current net savings meet or exceed target amount.
        """
        target_amount = float(goal.target_amount)
        current_savings = self.get_current_savings()

        needed_amount = target_amount - current_savings
        return max(0.00,needed_amount)