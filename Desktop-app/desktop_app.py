import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QListWidget, QListWidgetItem, QCalendarWidget, QDialog, QHBoxLayout
)
from PyQt6.QtCore import Qt
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

class AppointmentDialog(QDialog):
    """Popup window for booking an appointment"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book Appointment")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # Customer Search
        self.search_label = QLabel("Search by Phone:")
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_customer)

        # Customer Info
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        self.new_customer_button = QPushButton("Create New Customer")
        self.new_customer_button.clicked.connect(self.create_customer)

        # Appointment Calendar
        self.calendar_label = QLabel("Select Appointment Date:")
        self.calendar = QCalendarWidget()
        
        # Book Button
        self.book_button = QPushButton("Book Appointment")
        self.book_button.clicked.connect(self.book_appointment)

        # Layout
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.new_customer_button)
        layout.addWidget(self.calendar_label)
        layout.addWidget(self.calendar)
        layout.addWidget(self.book_button)

        self.setLayout(layout)

    def search_customer(self):
        phone = self.search_input.text()
        response = requests.get(f"{API_URL}/customers/search?phone={phone}")
        data = response.json()

        if "error" in data:
            QMessageBox.warning(self, "Error", "Customer not found!")
        else:
            self.name_input.setText(data["name"])
            self.phone_input.setText(data["phone"])
            self.customer_id = data["id"]

    def create_customer(self):
        name = self.name_input.text()
        phone = self.phone_input.text()

        if not name or not phone:
            QMessageBox.warning(self, "Error", "Please enter name and phone number.")
            return

        response = requests.post(f"{API_URL}/customers/create", json={"name": name, "phone": phone})
        data = response.json()

        if "error" in data:
            QMessageBox.warning(self, "Error", data["error"])
        else:
            QMessageBox.information(self, "Success", "Customer created successfully!")
            self.customer_id = data["customer"]["id"]

    def book_appointment(self):
        if not hasattr(self, "customer_id"):
            QMessageBox.warning(self, "Error", "Please select a customer first!")
            return

        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        response = requests.post(f"{API_URL}/appointments/book", json={
            "customer_id": self.customer_id,
            "appointment_time": selected_date
        })

        if response.status_code == 200:
            QMessageBox.information(self, "Success", "Appointment booked successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Failed to book appointment.")

class InventoryApp(QWidget):
    """Main Inventory Management Application"""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gemach Management")
        self.setGeometry(100, 100, 600, 500)

        layout = QVBoxLayout()

        # Open Appointment Booking
        self.appointment_button = QPushButton("Book Appointment")
        self.appointment_button.clicked.connect(self.open_appointment_dialog)

        layout.addWidget(self.appointment_button)

        self.setLayout(layout)

    def open_appointment_dialog(self):
        dialog = AppointmentDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
