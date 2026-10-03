from dataclasses import dataclass
from features.savings_management.service import SavingsService

@dataclass
class Goal:
    title: str
    target_amount: float|str
    target_date: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.id = self.id
        self.title = str(self.title).strip()
        self.target_date = str(self.target_date).strip()

        if not self.title:
            raise ValueError ("goal Title cannot be empty")
        if self.target_amount == "" or self.target_amount is None:
            raise ValueError ("Target amount cannot be empty")
        if not self.target_date:
            raise ValueError ("Target date cannot be empty")

        #i just call the function valid_amount from savingservice for code reusability
        self.target_amount = SavingsService.validate_amount(self.target_amount)
