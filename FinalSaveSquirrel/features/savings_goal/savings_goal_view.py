from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDoubleSpinBox, QDateEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox, QDialog, QScrollArea, QWidget
)
from PyQt6.QtGui import QFont , QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt , QDate

from features.savings_goal.service3 import ServiceGoal
from features.savings_goal.model3 import Goal
from features.savings_management.service import SavingsService
from features.savings_management.history_page_view import HistoryPage

msg_font = QFont("Arial", 11)
#this is the style sheet for qmessagebox
white_bg_style = """
                                   QMessageBox {
                                       background-color: #5c826f;
                                   }
                                   QMessageBox QLabel {
                                       color: white;
                                       background-color: transparent;
                                       border: none;
                                   }
                                   QMessageBox QPushButton { 
                                       background-color: #ffffff; 
                                       color: #19572a; 
                                       border-radius: 4px; 
                                       min-width: 30px;
                                       min-height: 10px;
                                       font-weight: bold; 
                                       border: none;
                                   }
                                   QMessageBox QPushButton:hover { 
                                       background-color: #e0f2f1; 
                                   }
                               """

class SavingsGoalPage(QFrame):
    def __init__(self, service_goal: ServiceGoal):
        super().__init__()
        self.service_goal = service_goal
        self.setStyleSheet("""
                    SavingsGoalPage {
                        background-color: white; 
                        border-radius: 10px; 
                        padding: 12px;
                    }
                    QPushButton {
                        background-color: #19572a;
                        color: white;
                        border-radius: 5px;
                        padding: 6px 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #144421;
                    }
                """)
        self.init_ui()

    def init_ui(self):

        self.goal_layout = QVBoxLayout()
        self.setLayout(self.goal_layout)
        self.goal_layout.addSpacing(20)

        header_layout = QHBoxLayout()

        #Main page header title
        self.savingsgoal_label = QLabel("Add Goals", self)
        self.savingsgoal_label.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.savingsgoal_label.setStyleSheet("color: #19572a;")
        header_layout.addWidget(self.savingsgoal_label)
        self.goal_layout.addLayout(header_layout)

        #this is for adding  a goals
        self.goalButton = QPushButton("Add Goal", self)
        self.goalButton.setFixedHeight(40)
        self.goalButton.setFixedWidth(120)
        self.goalButton.clicked.connect(self.goals_box)
        self.goalbtn_layout = QHBoxLayout()
        self.goalbtn_layout.addWidget(self.goalButton, alignment=Qt.AlignmentFlag.AlignRight)
        self.goal_layout.addLayout(self.goalbtn_layout)

        #this is the container for storing item list goals
        self.goal_card = QFrame()
        self.goal_card.setStyleSheet("background-color: white; border: 1px solid #e0f2f1;")
        self.goal_card.setMinimumSize(600, 450)

        goals_frame_layout = QVBoxLayout(self.goal_card)

        self.goals_label = QLabel("Active Goals", self)
        self.goals_label.setFont(QFont('Arial', 15, weight=QFont.Weight.Bold))
        self.goals_label.setStyleSheet("color: #19572a; border: none;")
        self.goals_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        goals_frame_layout.addWidget(self.goals_label)

        #this is the scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setStyleSheet("background-color: transparent; border: none; outline: none;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent; border: none;")
        self.goals_layout = QVBoxLayout(self.scroll_content)
        self.goals_layout.setSpacing(5)
        self.goals_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scrollArea.setWidget(self.scroll_content)
        goals_frame_layout.addWidget(scrollArea)

        self.goal_layout.addWidget(self.goal_card)
        self.goal_layout.addStretch()
        self.clear_goals()

#this is the UI for adding goals
#display pop up dialog for creating or adding a new goal
    def goals_box(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Savings Goal")
        dialog.setStyleSheet("background-color: #E8F5E9")
        dialog.setFixedSize(320, 380)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(4)
        layout.setContentsMargins(20, 20, 20, 20)

        self.head_label = QLabel("Add Savings Goal")
        self.head_label.setFont(QFont('Arial', 14, weight=QFont.Weight.Bold))
        self.head_label.setStyleSheet("color: #19572a;")
        self.head_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.head_label)

        layout.addSpacing(20)

        #this field is for the goal set title
        self.goalTitle = QLabel("Goal Title", self)
        self.goalTitle.setFont(QFont('Arial', 10, weight=QFont.Weight.Bold))
        self.goalTitle.setStyleSheet("color: #19572a;")
        layout.addWidget(self.goalTitle)

        self.title = QLineEdit()
        self.title.setStyleSheet("color: #19572a; font-size: 12px; background-color: white;")
        layout.addWidget(self.title)

        #this field is for the target amount
        self.goal_amount = QLabel("Target Amount", self)
        self.goal_amount.setFont(QFont('Arial', 10, weight=QFont.Weight.Bold))
        self.goal_amount.setStyleSheet("color: #19572a;")
        layout.addWidget(self.goal_amount)

        self.target_amount = QLineEdit()
        self.target_amount.setStyleSheet("color: #19572a; font-size: 12px; background-color: white;")
        layout.addWidget(self.target_amount)

        #this field is for the target date
        self.date_label = QLabel("Target Date", self)
        self.date_label.setFont(QFont('Arial', 10, weight=QFont.Weight.Bold))
        self.date_label.setStyleSheet("color: #19572a;")
        layout.addWidget(self.date_label)

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setCalendarPopup(True)
        self.date_box.setStyleSheet("color: #19572a; font-size: 12px; background-color: white;")
        layout.addWidget(self.date_box)

        layout.addStretch()

        add_goal_btn = QPushButton("Add Goal")
        add_goal_btn.setFixedHeight(35)
        add_goal_btn.setStyleSheet("background-color: #22573a;")
        add_goal_btn.clicked.connect(lambda: self.adding_goal(dialog))

        layout.addWidget(add_goal_btn)
        dialog.exec()

#this is for displaying your active goals
    def goals_frame(self, goals : Goal):
        item_frame_goal = QFrame()
        item_frame_goal.setFixedHeight(80)
        item_frame_goal.setStyleSheet("background-color: #f8fbf9; border: 1px solid #e0f2f1; border-radius: 8px;")

        item_goal_layout = QHBoxLayout(item_frame_goal)
        item_goal_layout.setContentsMargins(10, 0, 10, 0)
        item_goal_layout.setSpacing(8)
        item_goal_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        #Icon
        icon_label = QLabel("G")
        icon_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"background-color: #a0dec4; color: green; border-radius: 0px; border: none;")
        item_goal_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignVCenter)

        # Goal Title & Formatted ID Label Container
        text_container = QWidget()
        text_container.setStyleSheet("background-color: transparent; border: none;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setSpacing(1)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        title_label = QLabel(str(goals.title))
        title_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; margin: 0px; padding: 0px;")

        try:
            formatted_id = f"ID: #G{int(goals.id):05d}"
        except (ValueError, TypeError):
            formatted_id = f"ID: #{goals.id}"

        id_label = QLabel(formatted_id)
        id_label.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
        id_label.setStyleSheet("color: #19572a; border: none; margin: 0px; padding: 0px;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(id_label)
        item_goal_layout.addWidget(text_container)

        # Formatted Target Amount (₱) and Target Date Display Container
        amount_date_container = QWidget()
        amount_date_container.setStyleSheet("background-color: transparent; border: none;")

        amount_date_layout = QVBoxLayout(amount_date_container)
        amount_date_layout.setContentsMargins(0, 0, 0, 0)
        amount_date_layout.setSpacing(1)
        amount_date_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        formatted_amount = f"₱{float(goals.target_amount):,.2f}"
        amount_label = QLabel(formatted_amount)
        amount_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        amount_label.setStyleSheet(f"color: black; border: none; margin: 0px; padding: 0px;")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        target_date_str = str(goals.target_date) if goals.target_date else ""
        date = QDate.fromString(target_date_str, "yyyy-MM-dd")
        formatted_date = date.toString("MMM dd, yyyy") if date.isValid() else target_date_str

        date_label = QLabel(f"Target Date: {formatted_date}")
        date_label.setFont(QFont("Arial", 8))
        date_label.setStyleSheet("color: gray; border: none; margin: 0px; padding: 0px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        amount_date_layout.addWidget(amount_label)
        amount_date_layout.addWidget(date_label)

        item_goal_layout.addWidget(amount_date_container, 1, Qt.AlignmentFlag.AlignVCenter)

        #this are the button container
        btn_container = QWidget()
        btn_container.setStyleSheet("background-color: transparent; border: none;")
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(4, 0, 0, 0)
        btn_layout.setSpacing(4)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        #this is for the view button
        view_button = QPushButton("View")
        view_button.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
        view_button.setFixedSize(70, 26)
        view_button.setStyleSheet("""
                                                QPushButton {
                                                    background-color: #0ea131; 
                                                    color: white; 
                                                    border-radius: 4px;
                                                    border: none;
                                                    padding: 0px;
                                                }
                                                QPushButton:hover {
                                                    background-color: #0b8027;
                                                }
                                            """)

        view_button.clicked.connect(
            lambda checked, obj=goals: self.view(obj)
        )

        #this is the delete button
        delete_button = QPushButton("Delete")
        delete_button.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
        delete_button.setFixedSize(70, 26)
        delete_button.setStyleSheet("""
                                                QPushButton {
                                                    background-color: #a1270e; 
                                                    color: white; 
                                                    border-radius: 4px;
                                                    border: none;
                                                    padding: 0px;
                                                }
                                                QPushButton:hover {
                                                    background-color: #801f0b;
                                                }
                                            """)
        delete_button.clicked.connect(
            lambda checked, obj=goals, widget=item_frame_goal: self.delete(obj, widget)
        )

        btn_layout.addWidget(view_button)
        btn_layout.addWidget(delete_button)

        item_goal_layout.addWidget(btn_container, 0, Qt.AlignmentFlag.AlignVCenter)
        self.goals_layout.addWidget(item_frame_goal)

    def adding_goal(self, dialog) -> None:
        #read the input fields, and validates
        goal_title = self.title.text()
        target_amount = self.target_amount.text()
        target_date = self.date_box.date().toString("yyyy-MM-dd")

        try:
            new_goals = Goal(
                title=goal_title,
                target_amount=target_amount,
                target_date=target_date)
        except ValueError as e:
            msg = QMessageBox(QMessageBox.Icon.Warning, "Invalid Input", str(e))
            msg.setFont(msg_font)
            msg.setStyleSheet(white_bg_style)
            msg.exec()
            return

        #for confirmation
        msg = QMessageBox(
            QMessageBox.Icon.Question,
            "Confirm",
            "Are you sure you want to save this goal?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,

        )
        msg.setFont(msg_font)
        msg.setStyleSheet(white_bg_style)
        #confirmation
        if msg.exec() == QMessageBox.StandardButton.Yes:

            self.service_goal.add_goal(new_goals) #if success, add new_goals

            info_msg = QMessageBox(
                QMessageBox.Icon.Information, "Success", "Goals saved successfully!"
            )
            info_msg.setFont(msg_font)
            info_msg.setStyleSheet(white_bg_style)
            info_msg.exec()

            #clearing input fields
            self.title.clear()
            self.target_amount.clear()
            self.date_box.setDate(QDate.currentDate())
            self.clear_goals()
            dialog.accept()

        else:
            cancel_msg = QMessageBox(
                QMessageBox.Icon.Information, "Message", "Goal Cancelled"
            )

            cancel_msg.setFont(msg_font)
            cancel_msg.setStyleSheet(white_bg_style)
            cancel_msg.exec()

    def delete(self, goals : Goal, item_widget) -> None:
        """Prompts for deletion confirmation, deletes the record from DB, and removes widget from UI."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete this goal? #G{goals.id:05d}?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.setFont(msg_font)
        msg.setStyleSheet(white_bg_style)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.service_goal.delete_goals(goals.id)
            self.clear_goals()

            self.goals_layout.removeWidget(item_widget)
            item_widget.deleteLater()

    def clear_goals(self) -> None:
        # Clear existing widgets from the layout to avoid duplicate UI items
        HistoryPage.clear_layout(self.goals_layout)

        # Fetch goals from the database via ServiceGoal
        goals = self.service_goal.get_goals()

        for goal in goals:
            self.goals_frame(goal)

#this is for viewing goals, including viewing deadlines and needed amounts for that certain goals
    def view(self, goal : Goal) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Savings Goal - {goal.title}")
        dialog.setStyleSheet("background-color: #E8F5E9")
        dialog.setFixedSize(400, 380)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(4)
        layout.setContentsMargins(20, 20, 20, 20)

        formatted_id = f"#T{int(goal.id):05d}"

        self.label = QLabel(f"{goal.title}\n({formatted_id})")
        self.label.setFont(QFont('Arial', 14, weight=QFont.Weight.Bold))
        self.label.setStyleSheet("color: #19572a;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label)

        layout.addSpacing(20)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        target_value = QLabel(f"₱{float(goal.target_amount):,.2f}")
        target_value.setFont(QFont("Arial", 11, weight=QFont.Weight.Bold))
        target_value.setStyleSheet("color: #2c3e50;")

        date_value = QLabel(goal.target_date)
        date_value.setFont(QFont("Arial", 11))
        date_value.setStyleSheet("color: #2c3e50;")

        # Request dynamic calculations from ServiceGoal
        remaining_days = self.service_goal.get_remaining_days_text(goal.target_date)
        days_remain = QLabel(remaining_days)
        days_remain.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        days_remain.setStyleSheet("color: #19572a;")

        needed_amount = self.service_goal.needed_amount(goal)
        needed_val = QLabel(f"₱{needed_amount:,.2f}")
        needed_val.setFont(QFont("Arial", 11, weight=QFont.Weight.Bold))
        needed_val.setStyleSheet("color: #a1270e;")

        form_layout.addRow(
            QLabel("Target Amount:", font=QFont("Arial", 10) , styleSheet="color: black;"), target_value
        )
        form_layout.addRow(
            QLabel("Target Date:", font=QFont("Arial", 10), styleSheet="color: black;"), date_value
        )
        form_layout.addRow(
            QLabel("Remaining Days:", font=QFont("Arial", 10) , styleSheet="color: black;"), days_remain
        )
        form_layout.addRow(
            QLabel("Needed Amount:", font=QFont("Arial", 10) , styleSheet="color: black;"), needed_val
        )

        layout.addLayout(form_layout)
        layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(35)
        close_btn.setStyleSheet(
            "background-color: #22573a; color: white; font-weight: bold; border-radius: 5px;"
        )
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.exec()