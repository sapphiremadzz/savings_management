from dataclasses import dataclass

@dataclass
class SavingsDashboard:
    income: float
    expense: float
    savings: float

    def __post_init__(self) -> None:
        self.income = float(self.income)
        self.expense = float(self.expense)
        self.savings = float(self.savings)

