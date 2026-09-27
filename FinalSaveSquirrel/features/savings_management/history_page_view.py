import sys
from PyQt6.QtWidgets import (QLabel, QWidget, QPushButton, QFrame, QComboBox, QMessageBox, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QScrollArea, QDialog, QTabWidget)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate

from features.savings_management.service import SavingsService
from features.savings_management.model import Savings
from features.savings_management.repository import SavingsRepository
from features.savings_management.transaction_page_view import TransactionPage

msg_font = QFont("Arial", 11)
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

# THIS CLASS IS FOR HISTORY UI
class HistoryPage(QFrame):

    def __init__(self, service: SavingsService):
        super().__init__()
        self.service = service
        self.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        self.all_transactions_cache = []
        self.initUI()

        self.load_history()

    def initUI(self) -> None:

        history_layout = QVBoxLayout()
        self.setLayout(history_layout)

        self.history_label = QLabel("Transaction History", self)
        self.history_label.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.history_label.setStyleSheet("color: #19572a;")
        self.history_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        history_layout.addWidget(self.history_label)

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("🔍 Search history by UID or category...")
        self.search_bar.setFont(QFont("Arial", 10))
        self.search_bar.setStyleSheet("background-color: white; color:black; border: 1px solid #e0f2f1;")
        self.search_bar.textChanged.connect(self.filter_history)
        history_layout.addWidget(self.search_bar)

        history_frame = QFrame()
        history_frame.setStyleSheet("background-color: white; border: 1px solid #e0f2f1;")
        history_frame.setMinimumSize(600, 500)

        historyFrame_layout = QVBoxLayout(history_frame)
        historyFrame_layout.setContentsMargins(5, 5, 5, 5)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none; outline: none;")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: transparent; border: none;")
        self.historyTransaction_layout = QVBoxLayout(self.scroll_content)
        self.historyTransaction_layout.setSpacing(8)
        self.historyTransaction_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.scroll_content)
        historyFrame_layout.addWidget(scroll)
        history_layout.addWidget(history_frame)
        history_layout.addStretch()

    def add_historyCard(self, transaction: Savings, show_buttons=False):

        # this is fot the recent transaction card
        # this frame serves as the cards or box for viewing every records
        self.item_frame = QFrame()
        self.item_frame.setMinimumHeight(80)
        self.item_frame.setStyleSheet("background-color: #f8fbf9; border: 1px solid #e0f2f1; border-radius: 8px;")

        item_layout = QHBoxLayout(self.item_frame)
        item_layout.setContentsMargins(10, 4, 10, 4)
        item_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # this is something like a logo, and the icon will just display the first letter of each category in uppercase
        # category[0] means the first index of the letter
        is_expense = str(transaction.trans_type).lower() == "expense"
        icon_letter = transaction.category[0].upper() if transaction.category else "T"
        bg_color = "#fde8e8" if is_expense else "#e8f5e9"
        fg_color = "#ad5a61" if is_expense else "#2e7d32"

        icon_label = QLabel(icon_letter)
        icon_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"background-color: {bg_color}; color: {fg_color}; border-radius: 20px; border: none;")

        # this part is for the Category and UID
        text_container = QWidget()
        text_container.setStyleSheet("background-color: transparent; border: none;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setSpacing(0)
        text_layout.setContentsMargins(5, 0, 0, 0)

        title_label = QLabel(transaction.category)
        title_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; margin: 0px; padding: 0px;")

        try:
            formatted_id = f"ID: #{int(transaction.id):06d}"
        except (ValueError, TypeError):
            formatted_id = f"ID: #{transaction.id}"

        id_label = QLabel(formatted_id)
        id_label.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
        id_label.setStyleSheet("color: #19572a; border: none; margin: 0px; padding: 0px;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(id_label)

        """I set the description into optional, if the users didnt input something on the description     
                only the category and UID will be displayed"""
        if transaction.description:
            desc_label = QLabel(f"Note: {transaction.description}")
            desc_label.setFont(QFont("Arial", 8, italic=True))
            desc_label.setStyleSheet("color: #4a5568; border: none; margin: 0px; padding: 0px;")
            text_layout.addWidget(desc_label)

        # this is for the formatted date and amount with prefix + for income and - for expense
        amount_date_container = QWidget()
        amount_date_container.setStyleSheet("background-color: transparent; border: none;")

        amount_date_layout = QVBoxLayout(amount_date_container)
        amount_date_layout.setContentsMargins(0, 0, 0, 0)
        amount_date_layout.setSpacing(2)

        prefix = "-" if is_expense else "+"
        amount_color = "#630903" if is_expense else "#03632e"

        amount_label = QLabel(f"{prefix}{transaction.amount:,.2f}")
        amount_label.setFont(QFont("Arial", 11, weight=QFont.Weight.Bold))
        amount_label.setStyleSheet(f"color: {amount_color}; border: none;")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Dito i-adjust ang alignment!

        date = QDate.fromString(transaction.date, "yyyy-MM-dd")
        formatted_date = date.toString("MMM dd, yyyy") if date.isValid() else transaction.date

        date_label = QLabel(f"· {formatted_date}")
        date_label.setFont(QFont("Arial", 8))
        date_label.setStyleSheet("color: gray; border: none;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)  # Dito rin i-adjust ang alignment!

        amount_date_layout.addWidget(amount_label)
        amount_date_layout.addWidget(date_label)

        item_layout.addWidget(icon_label)
        item_layout.addWidget(text_container)
        item_layout.addStretch()
        item_layout.addWidget(amount_date_container)


        if show_buttons:
            item_layout.addSpacing(10)
            update_button = QPushButton("Update")
            update_button.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
            update_button.setFixedSize(75, 28)
            update_button.setStyleSheet("""
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



            update_button.clicked.connect(
                lambda checked, obj=transaction: self.update_historyClicked(obj)
            )

            delete_button = QPushButton("Delete")
            delete_button.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
            delete_button.setFixedSize(75, 28)
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
                lambda checked, obj=transaction, widget=self.item_frame: self.delete_historyClicked(obj, widget)
            )

            item_layout.addWidget(update_button)
            item_layout.addWidget(delete_button)

        return self.item_frame


    def add_history(self, transaction: Savings, show_buttons=True):

        item_frame = self.add_historyCard(transaction=transaction,
            show_buttons=show_buttons)
        self.historyTransaction_layout.addWidget(item_frame)


    def delete_historyClicked(self , transaction : Savings, item_widget):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete transaction #{transaction.id:06d}?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.setFont(msg_font)
        msg.setStyleSheet(white_bg_style)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.service.delete(transaction.id)

            self.historyTransaction_layout.removeWidget(item_widget)
            item_widget.deleteLater()

            if self.historyTransaction_layout.count() == 0:
                self.load_history()

    def update_historyClicked(self, transaction: Savings):

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Update Transaction #{transaction.id:06d}")
        dialog.setStyleSheet("background-color: #f5fcf9; border-radius: 8px;")
        dialog_layout = QVBoxLayout(dialog)

        edit_page = TransactionPage(service=self.service)

        edit_page.setStyleSheet("background-color: #f5fcf9; border-radius: 8px;")
        edit_page.transaction_label.setText(f"Edit Transaction #{transaction.id:06d}")
        edit_page.transaction_label.setFont(QFont('Arial', 20, weight=QFont.Weight.Bold))
        edit_page.transaction_box.setStyleSheet("background-color: #f5fcf9; border-radius: 8px;")

        edit_page.transaction_box.setFixedSize(480, 500)
        edit_page.transaction_box.setContentsMargins(2, 0, 0, 0)
        edit_page.comboType.setFont(QFont('Arial', 10))
        edit_page.comboCategory.setFont(QFont('Arial', 10))
        edit_page.edit_amount.setFont(QFont('Arial', 10))
        edit_page.edit_description.setFont(QFont('Arial', 10))


        type_idx = edit_page.comboType.findText(transaction.trans_type)
        if type_idx != -1:
            edit_page.comboType.setCurrentIndex(type_idx)
            edit_page.updateType_combo(type_idx)

        cat_idx = edit_page.comboCategory.findText(transaction.category)
        if cat_idx != -1:
            edit_page.comboCategory.setCurrentIndex(cat_idx)

        edit_page.comboType.currentIndexChanged.connect(edit_page.updateType_combo)

        edit_page.edit_amount.setText(str(transaction.amount))
        edit_page.edit_description.setText(transaction.description if transaction.description else "")

        qdate = QDate.fromString(str(transaction.date), "yyyy-MM-dd")
        if qdate.isValid():
            edit_page.date_box.setDate(qdate)

        edit_page.submit_transaction.setText("Save Changes")
        edit_page.submit_transaction.clicked.disconnect()

        def save_changes():
            confirm_msg = QMessageBox(dialog)
            confirm_msg.setIcon(QMessageBox.Icon.Question)
            confirm_msg.setWindowTitle("Confirm Update")
            confirm_msg.setText(f"Are you sure you want to update transaction #{transaction.id:06d}?")
            confirm_msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            confirm_msg.setDefaultButton(QMessageBox.StandardButton.No)
            confirm_msg.setFont(msg_font)
            confirm_msg.setStyleSheet(white_bg_style)

            if confirm_msg.exec() != QMessageBox.StandardButton.Yes:
                return

            updated_savings = Savings(
                id=transaction.id,
                trans_type=edit_page.comboType.currentText(),
                category=edit_page.comboCategory.currentText(),
                amount=edit_page.edit_amount.text(),
                description=edit_page.edit_description.text(),
                date=edit_page.date_box.date().toString("yyyy-MM-dd")
            )

            try:
                self.service.update(updated_savings)
            except Exception as e:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Invalid Input")
                msg.setText(str(e))
                msg.setFont(msg_font)
                msg.setStyleSheet(white_bg_style)
                msg.exec()
                return

            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("Transaction updated!")
            msg.setFont(msg_font)
            msg.setStyleSheet(white_bg_style)
            msg.exec()

            dialog.accept()

        edit_page.submit_transaction.clicked.connect(save_changes)

        dialog_layout.addWidget(edit_page)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_history()

    def clear_history_layout(self):
        """Clears all item widgets from the scroll view."""
        while self.historyTransaction_layout.count() > 0:
            item = self.historyTransaction_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_history(self):
        """Fetches items from database helper and updates cached transactions."""
        self.all_transactions_cache = self.service.fetch_formatted_history(limit=None) or []
        self.filter_history()

    def filter_history(self):
        """Filters cached items instantly when user types in the search bar."""
        self.clear_history_layout()
        query = self.search_bar.text().strip().lower()

        # Apply search condition against category
        filtered_items = [
            item for item in self.all_transactions_cache
            if query in str(item.get("category", "")).lower()
        ]

        if not filtered_items:
            no_data_msg = "No matching transactions found" if query else "No transactions yet"
            no_data_label = QLabel(no_data_msg)
            no_data_label.setFont(QFont("Arial", 11, weight=QFont.Weight.Bold))
            no_data_label.setStyleSheet("color: #083b1f; border: none; padding: 20px;")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.historyTransaction_layout.addWidget(no_data_label)
            return

        for item in filtered_items:
            savings_obj = Savings(
                id=item["id"],
                trans_type=item.get("trans_type") or ("Expense" if item.get("is_expense") else "Income"),
                category=item["category"],
                amount=item["amount"],
                description=item.get("description", ""),
                date=item["date"]
            )
            self.add_history(savings_obj)
