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
#this is the stylesheet for Qmessagebox
white_bg_style = """
    QMessageBox {
        background-color: #5c826f;
    }
    QMessageBox QLabel {
        color: white;
        background-color: transparent;
        border: none;
        font-size: 13px;
    }
    QMessageBox QPushButton { 
        background-color: #ffffff; 
        color: #19572a; 
        border-radius: 4px; 
        min-width: 40px;
        min-height: 20px;
        padding: 4px 12px;
        font-weight: bold; 
        border: none;
    }
    QMessageBox QPushButton:hover { 
        background-color: #e0f2f1; 
    }
"""

# THIS CLASS IS FOR HISTORY VIEWING (WITH UI)
class HistoryPage(QFrame):

    def __init__(self, service: SavingsService):
        super().__init__()
        self.service = service
        self.setStyleSheet("background-color: white; border-radius: 10px; padding: 15px;")
        self.all_transactions_cache = [] #Local cache storing fetched transactions for fast filtering without repeated DB queries
        self.initUI()

        self.load_history()

    def initUI(self) -> None:
        #this is the main layout
        history_layout = QVBoxLayout()
        self.setLayout(history_layout)

        #Main page title header
        self.history_label = QLabel("Transaction History", self)
        self.history_label.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
        self.history_label.setStyleSheet("color: #19572a;")
        self.history_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        history_layout.addWidget(self.history_label)

        #This is the search bar, users type here to search for past transactions
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search history by UID or category...")
        self.search_bar.setFont(QFont("Arial", 10))
        self.search_bar.setStyleSheet("background-color: white; color:black; border: 1px solid #e0f2f1;")
        #signals and trigger filter_history dynamically whenever text changes in the search bar
        self.search_bar.textChanged.connect(self.filter_history)
        history_layout.addWidget(self.search_bar)

        #frame container for transaction history records
        history_frame = QFrame()
        history_frame.setStyleSheet("background-color: white; border: 1px solid #e0f2f1;")
        history_frame.setMinimumSize(600, 500)

        historyFrame_layout = QVBoxLayout(history_frame)
        historyFrame_layout.setContentsMargins(5, 5, 5, 5)

        #this is the scroll area which enable scrolling when transaction items count exceeds screen height
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: transparent; border: none; outline: none;")
        #contains the content widget inside the scroll area containing the actual transaction item cards
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
        # this is for showing the save transactions card
        # this frame serves as the cards or box for viewing every records
        # past and save transactions can be seen in this frame
        """
            Parameters:
                - transaction (Savings): The data object containing record values.
                - show_buttons (bool): Determines whether Update/Delete buttons are display.

            Returns:
                - QFrame: The constructed UI card widget.

            it is also for code reusability
                       """
        self.item_frame = QFrame()
        self.item_frame.setFixedHeight(80)
        self.item_frame.setStyleSheet("background-color: #f8fbf9; border: 1px solid #e0f2f1; border-radius: 8px;")

        item_layout = QHBoxLayout(self.item_frame)
        item_layout.setContentsMargins(10, 0, 10, 0)
        item_layout.setSpacing(8)
        item_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # this is something like a logo, and the icon will just display the first letter of each category in uppercase
        # category[0] means the first index of the letter
        is_expense = str(transaction.trans_type).lower() == "expense"
        icon_letter = str(transaction.category)[0].upper()
        #color coding icon for transaction type(Income vs Expense)
        bg_color = "#fde8e8" if is_expense else "#e8f5e9"
        fg_color = "#ad5a61" if is_expense else "#2e7d32"

        icon_label = QLabel(icon_letter)
        icon_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(f"background-color: {bg_color}; color: {fg_color}; border-radius: 0px; border: none;")
        item_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignVCenter)

        # this part is for the Category, formated UID, and description if applicable
        #another container for layouts ng saganun di magconflicts ang mga layouts
        text_container = QWidget()
        text_container.setStyleSheet("background-color: transparent; border: none;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setSpacing(1)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        title_label = QLabel(str(transaction.category) if transaction.category else "Uncategorized")
        title_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; margin: 0px; padding: 0px;")

        #parang ganito siya #T00001
        formatted_id = f"ID: #T{int(transaction.id):05d}"

        id_label = QLabel(formatted_id)
        id_label.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
        id_label.setStyleSheet("color: #19572a; border: none; margin: 0px; padding: 0px;")

        text_layout.addWidget(title_label)
        text_layout.addWidget(id_label)

        """I set the description into optional, if the users didnt input something on the description     
                only the category and UID will be displayed"""
        if transaction.description:
            desc_text = str(transaction.description)
            if len(desc_text) > 80:
                desc_text = desc_text[:80] + "..." #length of 80 characters only
            desc_label = QLabel(f"Note: {desc_text}")
            desc_label.setFont(QFont("Arial", 8, italic=True))
            desc_label.setStyleSheet("color: #4a5568; border: none; margin: 0px; padding: 0px;")
            text_layout.addWidget(desc_label)
        #stretch 1 means para mat space siya sa gitna
        item_layout.addWidget(text_container, 1, Qt.AlignmentFlag.AlignVCenter)

        # this is for the formatted and layout date and amount with prefix + for income and - for expense
        amount_date_container = QWidget()
        amount_date_container.setStyleSheet("background-color: transparent; border: none;")

        amount_date_layout = QVBoxLayout(amount_date_container)
        amount_date_layout.setContentsMargins(0, 0, 0, 0)
        amount_date_layout.setSpacing(1)
        amount_date_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Assign sign (+/-) and color based on Expense or Income type
        prefix = "-" if is_expense else "+"
        amount_color = "#630903" if is_expense else "#03632e"

        formatted_amount = f"{prefix}{transaction.amount}"

        amount_label = QLabel(formatted_amount)
        amount_label.setFont(QFont("Arial", 10, weight=QFont.Weight.Bold))
        amount_label.setStyleSheet(f"color: {amount_color}; border: none; margin: 0px; padding: 0px;")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        raw_date_str = str(transaction.date)
        date = QDate.fromString(raw_date_str, "yyyy-MM-dd")
        formatted_date = date.toString("MMM dd, yyyy") if date.isValid() else raw_date_str

        date_label = QLabel(formatted_date)
        date_label.setFont(QFont("Arial", 8))
        date_label.setStyleSheet("color: gray; border: none; margin: 0px; padding: 0px;")
        date_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        amount_date_layout.addWidget(amount_label)
        amount_date_layout.addWidget(date_label)

        item_layout.addWidget(amount_date_container, 0, Qt.AlignmentFlag.AlignVCenter)
        #puss buttons (Update and delete)
        if show_buttons:
            btn_container = QWidget()
            btn_container.setStyleSheet("background-color: transparent; border: none;")
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(4, 0, 0, 0)
            btn_layout.setSpacing(4)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            #Update Button
            update_button = QPushButton("Update")
            update_button.setFont(QFont("Arial", 8, weight=QFont.Weight.Bold))
            update_button.setFixedSize(70, 26)
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

            #Delete Button
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
                lambda checked, obj=transaction, widget=self.item_frame: self.delete_historyClicked(obj, widget)
            )

            btn_layout.addWidget(update_button)
            btn_layout.addWidget(delete_button)

            item_layout.addWidget(btn_container, 0, Qt.AlignmentFlag.AlignVCenter)

        return self.item_frame


    def add_history(self, transaction: Savings, show_buttons=True):
        item_frame = self.add_historyCard(transaction=transaction,
            show_buttons=show_buttons)
        self.historyTransaction_layout.addWidget(item_frame)

    def delete_historyClicked(self , transaction : Savings, item_widget):
        """Handles deletion process for a transaction item.
            Prompt user for confirmation, removes record from DB, and destroys the card widget.
                """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle("Confirm Delete")
        msg.setText(f"Are you sure you want to delete transaction #{transaction.id:06d}?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        msg.setFont(msg_font)
        msg.setStyleSheet(white_bg_style)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.service.delete(transaction.id) #madelete ni siya from database

            # purpose ani is to delete a frame from UI layout and free some space
            self.historyTransaction_layout.removeWidget(item_widget)
            item_widget.deleteLater()

            #Reload cache if layout becomes empty
            if self.historyTransaction_layout.count() == 0:
                self.load_history()

    def update_historyClicked(self, transaction: Savings):

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Update Transaction #{transaction.id:06d}")
        dialog.setStyleSheet("background-color: #f5fcf9; border-radius: 8px;")
        dialog_layout = QVBoxLayout(dialog)

        edit_page = TransactionPage(service=self.service) #just reused the code UI from transactionPage ginawa ko lang qdialog
        #just change a little
        edit_page.setStyleSheet("background-color: #f5fcf9; border-radius: 8px;")
        edit_page.transaction_label.setText(f"Edit Transaction #{transaction.id:06d}")
        edit_page.transaction_label.setFont(QFont('Arial', 20, weight=QFont.Weight.Bold))
        edit_page.transaction_box.setStyleSheet("background-color: #f5fcf9; border-radius: 8px;")

        edit_page.transaction_box.setFixedSize(480, 530)
        edit_page.transaction_box.setContentsMargins(2, 0, 0, 0)
        edit_page.comboType.setFont(QFont('Arial', 10))
        edit_page.comboCategory.setFont(QFont('Arial', 10))
        edit_page.edit_amount.setFont(QFont('Arial', 10))
        edit_page.edit_description.setFont(QFont('Arial', 10))

        # Populate form fields with current transaction attributes
        # .findText() searches the comboType options for a match with transaction.trans_type.
        # If found, it returns the zero-based index (0, 1, etc.). If not found, it returns -1.
        type_idx = edit_page.comboType.findText(transaction.trans_type)
        if type_idx != -1:
            # Set the visible selection of the combo box to the matching index
            edit_page.comboType.setCurrentIndex(type_idx)
            # Manually trigger the helper function to reload/update the available categories
            # based on the selected type (e.g., loading Income categories vs Expense categories)
            edit_page.updateType_combo(type_idx)

        cat_idx = edit_page.comboCategory.findText(transaction.category)
        if cat_idx != -1:
            # Set the selected category in the dropdown to match the saved transaction's category
            edit_page.comboCategory.setCurrentIndex(cat_idx)

        # Attach a signals so if the user manually changes the combobox type (Income <-> Expense)
        # during editing, the category list will dynamically update to display matching options.
        edit_page.comboType.currentIndexChanged.connect(edit_page.updateType_combo)

        edit_page.edit_amount.setText(str(transaction.amount))
        edit_page.edit_description.setText(transaction.description if transaction.description else "")

        qdate = QDate.fromString(str(transaction.date), "yyyy-MM-dd")

        if qdate.isValid():
            edit_page.date_box.setDate(qdate)

        # Modify default button behavior for editing mode
        edit_page.submit_transaction.setText("Save Changes") #modify the label text of the button
        # Remove old signal connections
        # By default, clicking this button triggers the "Add New Transaction" method.
        # Disconnecting it ensures we don't accidentally create a duplicate record when saving edits.
        edit_page.submit_transaction.clicked.disconnect()

        def save_changes():
            raw_amount = edit_page.edit_amount.text()

            # check if the updated amount is valid
            try:
                valid = self.service.validate_amount(raw_amount)
            except  ValueError as e:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Invalid Input")
                msg.setText(str(e))
                msg.setFont(msg_font)
                msg.setStyleSheet(white_bg_style)
                msg.exec()
                return

            updated_savings = Savings(
                id=transaction.id,
                trans_type=edit_page.comboType.currentText(),
                category=edit_page.comboCategory.currentText(),
                amount=valid,
                description=edit_page.edit_description.text(),
                date=edit_page.date_box.date().toString("yyyy-MM-dd")
            )

            #confirm message dialog if all updated inputs are valid
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

            #saves updates to the database via service
            try:
                self.service.update(updated_savings)
            except Exception as e:
                msg = QMessageBox(dialog)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Error")
                msg.setText(str(e))
                msg.setFont(msg_font)
                msg.setStyleSheet(white_bg_style)
                msg.exec()
                return

            #this is for the success message
            msg = QMessageBox(dialog)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Success")
            msg.setText("Transaction updated!")
            msg.setFont(msg_font)
            msg.setStyleSheet(white_bg_style)
            msg.exec()

            dialog.accept()

        #Connect new save_changes to button
        edit_page.submit_transaction.clicked.connect(save_changes)

        dialog_layout.addWidget(edit_page)

        # I-Refresh ang page view after successful dialog acceptance
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_history()

    @staticmethod
    def clear_layout(layout):
        """Clears all item widgets from any given layout. This also make sure to avoid duplicate item frames"""
        #pag wala ni magduplicate ang mga UI frame
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def clear_history_layout(self):
        HistoryPage.clear_layout(self.historyTransaction_layout)

    def load_history(self):
        #calling the self.service.fetch_formatted_history() para kunin ang mga records sa data base
        # feed or kunin ang mga data galing sa service and update the all_transactions_caCHE
        self.all_transactions_cache = self.service.fetch_formatted_history(limit=None) or []
        self.filter_history()

    def filter_history(self):
        """Filters cached items instantly when user types in the search bar."""
        self.clear_history_layout()
        query = self.search_bar.text().strip().lower() #set lang sa lower para di case sensitive

        # Apply search condition against category and UID, set formatted ID so that when users type 0000, magshow up gihapon siya
        filtered_items = [
            item for item in self.all_transactions_cache
            if query in str(item.category).lower()
            or query in str(item.id).lower()
            or query in f"#T{item.id:05d}".lower()
        ]

        #if users search something on the search bar but hindi siya nakasave sa dataabse or wala sa itemframe
        #magdidisplay na no matchingtransactions found, or if wala pang transactions,no transactions yet ang lalabas

        if not filtered_items:
            no_data_msg = "No matching transactions found" if query else "No transactions yet"
            no_data_label = QLabel(no_data_msg)
            no_data_label.setFont(QFont("Arial", 11, weight=QFont.Weight.Bold))
            no_data_label.setStyleSheet("color: #083b1f; border: none; padding: 20px;")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.historyTransaction_layout.addWidget(no_data_label)
            return

        #display all transaction cards on the screen especially the mathching queries
        for item in filtered_items:
            self.add_history(item)