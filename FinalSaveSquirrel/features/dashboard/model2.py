class Dashboard:
    def __init__(self, income: float, expense: float, savings: float):
        # Private attributes (encapsulation) to protect total values from accidental modification
        self.__income = float(income)
        self.__expense = float(expense)
        self.__savings = float(savings)

#using getters to access this private attributes (Read Only)
    def get_income(self) -> float:
        return self.__income

    def get_expense(self) -> float:
        return self.__expense

    def get_savings(self) -> float:
        return self.__savings
