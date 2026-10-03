import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QFrame, QStackedWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from database.savings_database import SavingsDatabase
from features.savings_management.repository import SavingsRepository
from features.savings_management.service import SavingsService
from features.dashboard.service2 import DashboardService

from features.savings_management.history_page_view import HistoryPage
from features.dashboard.dashboard_page_view import DashboardPage
from features.savings_management.transaction_page_view import TransactionPage

from features.savings_goal.savings_goal_view import SavingsGoalPage
from features.savings_goal.repository3 import GoalRepository
from features.savings_goal.service3 import ServiceGoal

BUTTON_STYLE = """
    QPushButton {
        color: #19572a;
        background-color: transparent;
        font-size: 14px;
        padding: 12px 16px;
        text-align: center;
        border: none;
        border-radius: 8px;
        margin: 2px 10px;
    }
    QPushButton:hover {
        background-color: #d8ebd9;
        color: #19572a;
    }
    QPushButton:pressed {
        background-color: #c5e1c6;
    }
"""

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Savings Monitoring System")
        self.setGeometry(0, 0, 1100, 700)

        # Database and dependency injection sequence
        self.db = SavingsDatabase()
        self.repository = SavingsRepository(self.db)
        self.savings_service = SavingsService(self.repository)
        self.dashboard_service = DashboardService(self.repository)

        self.goal_repository = GoalRepository(self.db)
        self.goal_service = ServiceGoal(self.goal_repository, self.dashboard_service)

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(self.central_widget)

        main_frameLayout = QHBoxLayout()
        self.central_widget.setLayout(main_frameLayout)

        # this is for the side frame which you can see the menu, place on the left side of the window
        self.side_frame = QFrame()
        self.side_frame.setFixedWidth(200)
        self.side_frame.setStyleSheet("background-color: #E8F5E9; border-radius: 0px;")

        self.side_layout = QVBoxLayout()
        self.side_frame.setLayout(self.side_layout)

        self.label = QLabel("SaveSquirrel🐿", self)
        self.label.setFont(QFont('Arial', 15, weight=QFont.Weight.Bold))
        self.label.setStyleSheet("color: #19572a; padding: 10px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # these area the buttons of the sideframe

        self.dashboard_button = QPushButton("Dashboard", self)
        self.dashboard_button.setStyleSheet(BUTTON_STYLE)
        self.dashboard_button.clicked.connect(self.add_dashboardClicked)

        self.add_button = QPushButton("Add Transaction", self)
        self.add_button.setStyleSheet(BUTTON_STYLE)
        self.add_button.clicked.connect(self.add_buttonClicked)

        self.history_button = QPushButton("View / Edit History", self)
        self.history_button.setStyleSheet(BUTTON_STYLE)
        self.history_button.clicked.connect(self.add_historyClicked)

        self.goals_button = QPushButton("Savings Goals", self)
        self.goals_button.setStyleSheet(BUTTON_STYLE)
        self.goals_button.clicked.connect(self.add_goalsClicked)

        self.side_layout.addWidget(self.label)
        self.side_layout.addWidget(self.dashboard_button)
        self.side_layout.addWidget(self.add_button)
        self.side_layout.addWidget(self.history_button)
        self.side_layout.addWidget(self.goals_button)
        self.side_layout.addStretch()

        # Stacked widget , used for switching multiple pages... displaying one page a time
        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage(
            dashboard_service=self.dashboard_service,
            savings_service=self.savings_service
        )
        self.transaction_page = TransactionPage(
            service=self.savings_service,
            dashboard_page=self.dashboard_page
        )
        self.history_page = HistoryPage(
            service=self.savings_service
        )
        self.goals_page = SavingsGoalPage(
            service_goal=self.goal_service
        )

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.transaction_page)
        self.pages.addWidget(self.history_page)
        self.pages.addWidget(self.goals_page)

        # main window, the window that is visible to the screen
        main_frameLayout.addWidget(self.side_frame)  # this is the side frame
        main_frameLayout.addWidget(self.pages)  # this part switch depending on which button you clicked in the sideframe

    def add_dashboardClicked(self):
        self.dashboard_page.refresh_recent_transactions()  # refresh dashboard summary when user update or add something
        self.pages.setCurrentIndex(0)  # when the user click the dashboard button the dashboard window will display

    def add_buttonClicked(self):
        self.pages.setCurrentIndex(1)  # when the user click the add transaction button the transaction window will display

    def add_historyClicked(self):
        self.history_page.load_history()
        self.pages.setCurrentIndex(2)  # when the user click the view history button the view history window will display

    def add_goalsClicked(self):
        self.pages.setCurrentIndex(3)
        print("hello")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()