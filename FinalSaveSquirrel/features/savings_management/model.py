from dataclasses import dataclass

@dataclass
class Savings:
    trans_type: str
    category: str
    amount: float
    description: str | None
    date: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.id = self.id
        self.trans_type = self.trans_type.strip()
        self.category = self.category.strip()
        self.amount = float(self.amount)
        self.description = self.description or ""
        self.date = self.date.strip()

