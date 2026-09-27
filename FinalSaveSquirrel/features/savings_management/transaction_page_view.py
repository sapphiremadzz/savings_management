from PyQt6.QtWidgets import (QLabel, QWidget, QPushButton
, QFrame, QLineEdit, QComboBox, QMessageBox,
                             QVBoxLayout, QHBoxLayout, QGridLayout, QDateEdit, QTabWidget, QTableWidgetItem,
                             QTableWidget, QHeaderView, QAbstractItemView, QDialog)
from PyQt6.QtGui import QFont , QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt , QDate

from features.savings_management.service import  SavingsService
from features.savings_management.model import Savings

#dictionary, this is for the combobox
data = {
       "Income": ["Allowance", "Salary", "Pension", "Stipend", "Other"],
       "Expense": ["Transportation", "Food", "Bills" , "Travels" , "Shopping" , "Tuition", "Other"]
   }

#THIS CLASS IS FOR TRANSACTIONS UI
class TransactionPage(QFrame):
   def __init__(self , service : SavingsService , dashboard_page = None):
       super().__init__()
       self.service = service

       self.setStyleSheet("background-color: white; border-radius: 10px; padding: 12px;")

       self.dashboard_page = dashboard_page
       self.initUI()

   def initUI(self):
       self.transaction_layout = QVBoxLayout()
       self.setLayout(self.transaction_layout)

       # Main Page Title Header
       self.transaction_label = QLabel("Add Transaction", self)
       self.transaction_label.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))
       self.transaction_label.setStyleSheet("color: #19572a;")
       self.transaction_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

       self.transaction_layout.addWidget(self.transaction_label)
       self.transactionBox()

   def transactionBox(self) :
       self.transaction_box = QFrame()
       self.transaction_box.setStyleSheet("background-color: #c5e3ce; border-radius: 0px;")

       box_layout = QVBoxLayout()
       box_layout.setContentsMargins(20, 20, 20, 20)
       box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
       self.transaction_box.setLayout(box_layout)

       # this is the for combo box transaction window where the users select which type of transactions they want to submit
       type_cat_grid = QGridLayout()  # i used grid layout to align my labels and comboboxes for better interaction
       type_cat_grid.setSpacing(10)

       #labels for type and category
       self.type_label = QLabel("Type", self)
       self.type_label.setFont(QFont('Arial', 12, weight=QFont.Weight.Bold))
       self.type_label.setStyleSheet("color: #19572a;")
       self.type_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

       self.category_label = QLabel("Category", self)
       self.category_label.setFont(QFont('Arial', 12, weight=QFont.Weight.Bold))
       self.category_label.setStyleSheet("color: #19572a;")
       self.category_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

       # this is a dependent combobox
       self.model = QStandardItemModel()
       # QStandardItemModel used to display data from the comboboxes
       # this has a hierarchy structure, a parent-child structure

       # if user click the income on the combo box, its children will show up on the category
       self.comboType = QComboBox()
       self.comboType.setFont(QFont('Arial', 12))
       self.comboType.setStyleSheet("background-color: white;" "color: #19572a;"
                                    "border-radius: 5px;" "padding: 3px 10px;")
       self.comboType.setModel(self.model)

       self.comboCategory = QComboBox()
       self.comboCategory.setFont(QFont('Arial', 12))
       self.comboCategory.setStyleSheet("background-color: white;" "color: #19572a;"
                                        "border-radius: 5px;" "padding: 3px 10px;")
       self.comboCategory.setModel(self.model)

       # The following code loops through the dictionary
       for k, v in data.items():
           type = QStandardItem(k)
           self.model.appendRow(type)
           for value in v:
               category = QStandardItem(value)
               type.appendRow(category)

       self.comboType.currentIndexChanged.connect(self.updateType_combo)
       self.updateType_combo(0)  # this initially displays the income and its categories Allowance
       # The value 0 represents the first item in the ComboBox, which is Income.
       # herefore, when the form initially opens, the category ComboBox displays the categories under Income.

       type_cat_grid.addWidget(self.type_label, 0, 0)  # row 0, column 0
       type_cat_grid.addWidget(self.comboType, 1, 0)  # row 1, column 0
       type_cat_grid.addWidget(self.category_label, 0, 1)  # row 0, column 1
       type_cat_grid.addWidget(self.comboCategory, 1, 1)  # row 1, column 1

       # this is for typing the amount
       self.amount_label = QLabel("Enter amount", self)
       self.amount_label.setFont(QFont('Arial', 12, weight=QFont.Weight.Bold))
       self.amount_label.setStyleSheet("color: #19572a;")
       self.amount_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

       # this line the users will input the amount on the given textbox
       self.edit_amount = QLineEdit()
       self.edit_amount.setStyleSheet("color: #19572a; font-size: 12px; background-color: white;")

       type_layout = QHBoxLayout()
       type_layout.addWidget(self.type_label)
       type_layout.addWidget(self.category_label)

       amount_label_layout = QHBoxLayout()
       amount_label_layout.addWidget(self.amount_label)
       amount_layout = QHBoxLayout()
       amount_layout.addWidget(self.edit_amount)

       # this is for typing description , users will put the description of their transaction but it is also optional
       self.description_label = QLabel("Description", self)
       self.description_label.setFont(QFont('Arial', 12, weight=QFont.Weight.Bold))
       self.description_label.setStyleSheet("color: #19572a;")

       self.edit_description = QLineEdit()
       self.edit_description.setPlaceholderText("(optional)")
       self.edit_description.setStyleSheet("color: #19572a; font-size: 12px; background-color: white;")

       description_label_layout = QHBoxLayout()
       description_label_layout.addWidget(self.description_label)

       description_layout = QHBoxLayout()
       description_layout.addWidget(self.edit_description)

       self.date_label = QLabel("Date", self)
       self.date_label.setFont(QFont('Arial', 12, weight=QFont.Weight.Bold))
       self.date_label.setStyleSheet("color: #19572a;")

       self.date_box = QDateEdit()
       # QDateEdit is specifically designed to display and edit dates.
       self.date_box.setDate(QDate.currentDate())
       self.date_box.setCalendarPopup(True)  # this pop up the calendar
       self.date_box.setStyleSheet("color: #19572a; font-size: 12px; background-color: white;")

       date_label_layout = QHBoxLayout()
       date_label_layout.addWidget(self.date_label)

       date_layout = QHBoxLayout()
       date_layout.addWidget(self.date_box)

       # this is for the submitting of transactions, users will clicked the button if they wanted to submit their transaction
       self.submit_transaction = QPushButton("Submit Transaction", self)
       self.submit_transaction.setStyleSheet("color: white; font-size: 12px; background-color: #22573a;")
       self.submit_transaction.clicked.connect(self.add_transactionClicked)

       submit_button_layout = QHBoxLayout()
       submit_button_layout.addWidget(self.submit_transaction)

       # Append all input field sub-layouts sequentially into the main container frame
       # order really matters here, the top are the labels type and category and the bottom is the submit button
       box_layout.addLayout(type_cat_grid)
       box_layout.addLayout(amount_label_layout)
       box_layout.addLayout(amount_layout)
       box_layout.addLayout(description_label_layout)
       box_layout.addLayout(description_layout)
       box_layout.addLayout(date_label_layout)
       box_layout.addLayout(date_layout)
       box_layout.addLayout(submit_button_layout)

       self.transaction_layout.addWidget(self.transaction_box)
       self.transaction_layout.addStretch()

   # this function is responsible for changing the categories based on the selected transaction type.
   def updateType_combo(self, index):
       indx = self.model.index(index, 0, self.comboType.rootModelIndex())
       """sets the selected transaction type as the root index of the category ComboBox,
              allowing it to display only the child categories associated with that transaction type.
              so for example if users chooses expenses,
              then its categories [transportation, food, others] will display"""
       self.comboCategory.setRootModelIndex(
           indx)
       self.comboCategory.setCurrentIndex(0)

   # this part is on the transaction page where if the users click the submit button,
   # there is a messagebox that will pop up,
   def add_transactionClicked(self):
       self.validation()

   def validation(self):
       trans_type = self.comboType.currentText()
       category = self.comboCategory.currentText()
       amount_text = self.edit_amount.text()
       description = self.edit_description.text()
       dates = self.date_box.date().toString("yyyy-MM-dd")

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

       # Hand off logic and validation
       # before this save on the databases, we must validate if the amount enter is valid
       try:
           valid_amount = self.service.validate_amount(amount_text)
       except ValueError as e:
           msg = QMessageBox(QMessageBox.Icon.Warning, "Invalid Input", str(e), parent=self)
           msg.setFont(msg_font)
           msg.setStyleSheet(white_bg_style)
           msg.exec()
           return


       msg = QMessageBox(
           QMessageBox.Icon.Question,
           "Confirm",
           "Are you sure you want to submit this transaction?",
           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
           parent=self,
       )
       msg.setFont(msg_font)
       msg.setStyleSheet(white_bg_style)

       if msg.exec() == QMessageBox.StandardButton.Yes:

           new_savings = Savings(
               trans_type=trans_type,
               category=category,
               amount=valid_amount,
               description=description,
               date=dates
           )

           self.service.add_transaction(new_savings)

           if self.dashboard_page:
               self.dashboard_page.refresh_recent_transactions()

           info_msg = QMessageBox(
               QMessageBox.Icon.Information, "Success", "Transaction saved successfully!", parent=self
           )
           info_msg.setFont(msg_font)
           info_msg.setStyleSheet(white_bg_style)
           info_msg.exec()


           self.edit_amount.clear()
           self.edit_description.clear()
           self.date_box.setDate(QDate.currentDate())
           self.comboType.setCurrentIndex(0)
           self.updateType_combo(0)
       else:
           cancel_msg = QMessageBox(
               QMessageBox.Icon.Information, "Message", "Transaction Cancelled", parent=self
           )
           cancel_msg.setFont(msg_font)
           cancel_msg.setStyleSheet(white_bg_style)
           cancel_msg.exec()








