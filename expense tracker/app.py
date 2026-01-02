from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit,
    QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QPalette, QColor
from database import fetch_expenses, add_expenses, delete_expense


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
        self.setGeometry(300, 300, 550, 500)
        self.setWindowTitle("Expense Tracker App")

    def initUI(self):
        # Widgets
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton("Add Expense")
        self.btn_delete = QPushButton("Delete Expense")
        self.btn_delete.setEnabled(False)  # start disabled

        # Table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Date", "Category", "Amount", "Description"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Dropdown items
        self.populate_dropdown()

        # Connect signals
        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)
        self.table.itemSelectionChanged.connect(self.row_selected)

        # Object names for CSS
        self.btn_add.setObjectName("btn_add")
        self.btn_delete.setObjectName("btn_delete")

        # Table selection behavior
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)  # optional, looks nice

        # Palette fix for green selection
        palette = self.table.palette()
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#4caf50"))  # green
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        self.table.setPalette(palette)

        # Apply CSS
        self.apply_styles()

        # Layout
        self.setup_layout()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        row1.addWidget(QLabel("Date"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category"))
        row1.addWidget(self.dropdown)

        row2.addWidget(QLabel("Amount"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description"))
        row2.addWidget(self.description)

        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)

        self.setLayout(master)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e3e9f2;
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: #333;
            }

            QLabel {
                font-size: 16px;
                color: #2c3e50;
                font-weight: bold;
                padding: 5px;
            }

            QLineEdit, QComboBox, QDateEdit {
                background-color: #fff;
                font-size: 14px;
                color: #333;
                border: 1px solid #b0bfc6;
                border-radius: 15px;
                padding: 5px;
            }

            QLineEdit:hover, QComboBox:hover, QDateEdit:hover {
                border: 1px solid #4caf50;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 1px solid #2a9d8f;
                background-color: #f5f9fc;
            }

            QTableWidget {
                background-color: #fff;
                alternate-background-color: #f2f7fb;
                gridline-color: #c0c9d0;
                font-size: 14px;
                border: 1px solid #dfd9e1;
            }

            QHeaderView::section {
                background-color: #4caf50;
                color: white;
                padding: 5px;
                font-weight: bold;
                border: 1px solid #dfd9e1;
            }

            QPushButton#btn_add {
                background-color: #4caf50;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#btn_add:hover {
                background-color: #45a049;
            }

            QPushButton#btn_add:pressed {
                background-color: #3db840;
            }

            QPushButton#btn_delete {
                background-color: #e74c3c;
                color: white;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton#btn_delete:hover {
                background-color: #c0392b;
            }

            QPushButton#btn_delete:pressed {
                background-color: #a93226;
            }

            QPushButton:disabled {
                background-color: #c8c8c8;
                color: #6e6e6e;
            }

            QToolTip {
                background-color: #2c3e50;
                color: #ffffff;
                border: 1px solid #333;
                font-size: 12px;
                padding: 5px;
                border-radius: 4px;
            }
        """)

    def populate_dropdown(self):
        categories = ["Food", "Rent", "Bills", "Entertainment", "Shopping", "Other"]
        self.dropdown.addItems(categories)

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                item = QTableWidgetItem(str(data))
                # Make each cell selectable and enabled so selection works
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row_idx, col_idx, item)

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, "Input Error", "Amount and Description cannot be empty")
            return

        if add_expenses(date, category, amount, description):
            self.load_table_data()
            self.clear_inputs()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense")

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Uh oh", "You need to select a row to delete")
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(
            self, "Confirm",
            "Are you sure you want to delete?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes and delete_expense(expense_id):
            self.load_table_data()
            self.btn_delete.setEnabled(False)  # disable after deletion

    def row_selected(self):
        # Enable Delete button only when a row is selected
        if self.table.selectedItems():
            self.btn_delete.setEnabled(True)
        else:
            self.btn_delete.setEnabled(False)
