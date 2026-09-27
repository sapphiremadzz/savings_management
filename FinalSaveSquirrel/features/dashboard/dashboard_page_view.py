from PyQt6.QtWidgets import (QLabel , QWidget , QFrame , QLineEdit , QVBoxLayout , QHBoxLayout , QGridLayout
        , QScrollArea )
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt , QDate

from features.savings_management.history_page_view import HistoryPage
from features.dashboard.service2 import DashboardService
from features.savings_management.model import Savings
from features.savings_management.service import SavingsService

#THIS CLASS IS FOR DASHBOARD UI
class DashboardPage(QFrame):

    def __init__(self , dashboard_service: DashboardService, savings_service: SavingsService, parent=None):
        super().__init__(parent)
        self.dashboard_service = dashboard_service
        self.savings_service = savings_service
        self.setStyleSheet("background-color: white; border-radius: 10px; padding: 5px;")
        self.initUI()

        self.refresh_recent_transactions()

    def initUI(self) -> None:
        # Main vertical container for the entire dashboard page
        dashboard_layout = QVBoxLayout()
        self.setLayout(dashboard_layout)

        # this is the main frame of dashboard that will display on the screen
        self.dashboard_label = QLabel("Dashboard", self)
        self.dashboard_label.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.dashboard_label.setStyleSheet("color: #19572a;")  # this color is likely darkgreen

        self.dashboard_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.dashboard2_label = QLabel("Good Day, Squirrels!", self)
        self.dashboard2_label.setFont(QFont('Arial', 18, weight=QFont.Weight.Bold))
        self.dashboard2_label.setStyleSheet("color: #19572a;")
        self.dashboard2_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.dashboard3_label = QLabel("Here is an overview", self)
        self.dashboard3_label.setFont(QFont('Arial', 11))
        self.dashboard3_label.setStyleSheet("color: gray; padding: 10px;")
        self.dashboard3_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        #add labels to the main dashboard layout
        dashboard_layout.addWidget(self.dashboard_label)
        dashboard_layout.addWidget(self.dashboard2_label)
        dashboard_layout.addWidget(self.dashboard3_label)

#I used grid layout to align my cards
        dashboard_cardLayout = QGridLayout()
        dashboard_cardLayout.setContentsMargins(0, 0, 0, 0)

        # this is for the savings card
        self.savings_card = QFrame()
        self.savings_card.setStyleSheet("background-color: #f5fcf9; border-radius: 0px; "
                                        "border: 1px solid #e0f2f1;")

        savings_layout = QVBoxLayout()
        self.savings_card.setLayout(savings_layout)

        #Savings Label
        self.savings_label = QLabel("Savings", self)
        self.savings_label.setFont(QFont('Arial', 15, weight=QFont.Weight.Bold))
        self.savings_label.setStyleSheet("color: #19572a; border: none;")
        self.savings_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        #Savings text box amount,
        #0.00 is just a default value, when users add a transactions, the value will change
        self.savings_box = QLineEdit("$0.00")
        self.savings_box.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.savings_box.setStyleSheet("color: #5aad9e; border: none;")
        self.savings_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.savings_box.setReadOnly(True) #meaning users cant edit this section

        savings_layout.addWidget(self.savings_label)
        savings_layout.addWidget(self.savings_box)

        # this is for the income card
        self.income_card = QFrame()
        self.income_card.setStyleSheet("background-color: #f5fcf9; border-radius: 0px; "
                                       "border: 1px solid #e0f2f1;")

        income_layout = QVBoxLayout()
        self.income_card.setLayout(income_layout)

        self.income_label = QLabel("Income", self)
        self.income_label.setFont(QFont('Arial', 15, weight=QFont.Weight.Bold))
        self.income_label.setStyleSheet("color: #19572a; border: none;")
        self.income_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.income_box = QLineEdit("$0.00")
        self.income_box.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.income_box.setStyleSheet("color: #4872b5; border: none;")
        self.income_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.income_box.setReadOnly(True)

        income_layout.addWidget(self.income_label)
        income_layout.addWidget(self.income_box)

        # this is for the expense card
        self.expense_card = QFrame()
        self.expense_card.setStyleSheet("background-color: #f5fcf9; border-radius: 0px; "
                                        "border: 1px solid #e0f2f1;")
        expense_layout = QVBoxLayout()
        self.expense_card.setLayout(expense_layout)

        self.expense_label = QLabel("Expense", self)
        self.expense_label.setFont(QFont('Arial', 15, weight=QFont.Weight.Bold))
        self.expense_label.setStyleSheet("color: #19572a; border: none;")
        self.expense_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.expense_box = QLineEdit("$0.00")
        self.expense_box.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.expense_box.setStyleSheet("color: #ad5a61; border: none;")
        self.expense_box.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.expense_box.setReadOnly(True)

        expense_layout.addWidget(self.expense_label)
        expense_layout.addWidget(self.expense_box)

        # this layout is grid layout, display in horizontal way
        dashboard_cardLayout.setHorizontalSpacing(20)
        dashboard_cardLayout.addWidget(self.savings_card, 0, 0)
        dashboard_cardLayout.addWidget(self.income_card, 0, 1)
        dashboard_cardLayout.addWidget(self.expense_card, 0, 2)

        # Add the grid cards to the main dashboard layout
        dashboard_layout.addLayout(dashboard_cardLayout)
        dashboard_layout.addSpacing(20)

        # this is for the recent transactions card, it will display the top 20 recent records of users transaction
        self.recent_card = QFrame()
        self.recent_card.setStyleSheet("background-color: #f2f7f5; border-radius: 0px; border: none")
        self.recent_card.setMinimumSize(600, 330)

        recent_layout = QVBoxLayout(self.recent_card)

        self.recent_label = QLabel("Recent Transactions", self)
        self.recent_label.setFont(QFont('Arial', 15, weight=QFont.Weight.Bold))
        self.recent_label.setStyleSheet("color: #19572a; border: none;")
        self.recent_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        recent_layout.addWidget(self.recent_label)

        """acts as a viewport window. If the items inside exceed the available height, 
        it enables scrolling without stretching the entire application window."""
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("background-color: transparent; border: none; outline: none;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent; border: none;")
        self.recentTransactions_layout = QVBoxLayout(self.scroll_content)
        self.recentTransactions_layout.setSpacing(5)
        self.recentTransactions_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scrollArea.setWidget(self.scroll_content)
        recent_layout.addWidget(scrollArea)
        #Add recent transactions frame to main dashboard layout
        dashboard_layout.addWidget(self.recent_card)
        dashboard_layout.addStretch()

    def add_recentTransaction(self , transaction: Savings, show_buttons=False):

        history_edit = HistoryPage(service=self.savings_service)
        item_frame = history_edit.add_historyCard(
            transaction=transaction,
            show_buttons=show_buttons
        )
        item_frame.setMinimumHeight(100)

        #places the newest transaction at the very top of the layout container.
        self.recentTransactions_layout.addWidget(item_frame)

        """Ensures that the container holds a maximum of 20 items
        if the items reaches the maximum, the bottom item or the last item which is takeAt(count()-1)
        name oldest_item will deleted
        """
        while self.recentTransactions_layout.count() > 20:
            oldest_item = self.recentTransactions_layout.takeAt(self.recentTransactions_layout.count() -1)
            if oldest_item.widget():
                oldest_item.widget().deleteLater()

    def clear_recent_transactions(self):
        while self.recentTransactions_layout.count() > 0:
            item = self.recentTransactions_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_recent_transactions(self):
        """this function fetches latest database entries and populates the recent transactions feed."""
        self.clear_recent_transactions()
        recent_transactions = self.savings_service.fetch_formatted_history(limit=20)

        """if there is no transactions added, then the box will display No transactions
        but when users add transaction from transaction page, the default text will disappear
        and it will display the recent transactions ,limit to recent 20 items"""
        if not recent_transactions:
            no_data_label = QLabel("No transactions yet")
            no_data_label.setFont(QFont("Arial", 11, weight=QFont.Weight.Bold))
            no_data_label.setStyleSheet("color: #083b1f; border: none;")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.recentTransactions_layout.addWidget(no_data_label)
            return

        for item in recent_transactions:
            savings_obj = Savings(
                id=item["id"],
                trans_type=item.get("trans_type") or ("Expense" if item.get("is_expense") else "Income"),
                category=item["category"],
                amount=item["amount"],
                description=item.get("description", ""),
                date=item["date"]
            )
            self.add_recentTransaction(savings_obj, show_buttons=False)

    def refresh_recent_transactions(self):
        summary = self.dashboard_service.fetch_dashboard_summary()
        self.update_totals(summary.income, summary.expense, summary.savings)
        self.load_recent_transactions()

    def update_totals(self, income, expense, savings):
        """to update displayed totals in the dashboard dynamically whenever a new item is submitted."""
        self.income_box.setText(f"₱{income:,.2f}")
        self.expense_box.setText(f"₱{expense:,.2f}")
        self.savings_box.setText(f"₱{savings:,.2f}")