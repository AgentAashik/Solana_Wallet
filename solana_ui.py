import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from solana_wallet import create_wallet, get_balance, send_transaction

class SolanaWalletUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Solana Wallet")
        self.setGeometry(200, 200, 400, 500)  # Bigger window size

        self.setStyleSheet("""
            QWidget {
                background-color: #f8f5ff;
                color: #4A148C;
                font-family: 'Poppins', sans-serif;
            }
            QPushButton {
                background-color: #7B1FA2;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #6A1B9A;
            }
            QLineEdit {
                border: 2px solid #7B1FA2;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                background-color: #ffffff;
            }
        """)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("🚀 Solana Wallet")
        title.setFont(QFont("Poppins", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Create Wallet Button
        self.create_wallet_btn = QPushButton("Create New Wallet")
        self.create_wallet_btn.clicked.connect(self.create_wallet)
        layout.addWidget(self.create_wallet_btn)

        # Check Balance
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Enter Public Key")
        layout.addWidget(self.address_input)

        self.check_balance_btn = QPushButton("Check Balance")
        self.check_balance_btn.clicked.connect(self.check_balance)
        layout.addWidget(self.check_balance_btn)

        # Send SOL
        self.private_key_input = QLineEdit()
        self.private_key_input.setPlaceholderText("Enter Private Key")
        layout.addWidget(self.private_key_input)

        self.to_address_input = QLineEdit()
        self.to_address_input.setPlaceholderText("Enter Recipient Address")
        layout.addWidget(self.to_address_input)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter Amount (SOL)")
        layout.addWidget(self.amount_input)

        self.send_sol_btn = QPushButton("Send SOL")
        self.send_sol_btn.clicked.connect(self.send_sol)
        layout.addWidget(self.send_sol_btn)

        # Exit Button
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.setStyleSheet("background-color: #D32F2F; color: white; font-size: 16px;")
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

    def create_wallet(self):
        public_key, private_key = create_wallet()
        QMessageBox.information(self, "Wallet Created",
                                f"Public Key:\n{public_key}\n\nPrivate Key:\n{private_key}")

    def check_balance(self):
        address = self.address_input.text().strip()
        if not address:
            QMessageBox.warning(self, "Error", "Please enter a valid public key.")
            return

        balance = get_balance(address)
        QMessageBox.information(self, "Balance", f"Your balance: {balance} SOL")

    def send_sol(self):
        private_key = self.private_key_input.text().strip()
        to_address = self.to_address_input.text().strip()
        amount_text = self.amount_input.text().strip()

        if not private_key or not to_address or not amount_text:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            amount = float(amount_text)
            txn_hash = send_transaction(private_key, to_address, amount)
            if txn_hash is None:
                QMessageBox.showerror("Transaction Error", "An error occurred while sending SOL.")
                return  # Stop further execution
 
            if txn_hash.startswith("ERROR:"):
                QMessageBox.showerror("Transaction Error", txn_hash)
            else:
                QMessageBox.showinfo("Transaction Successful", f"Transaction ID:\n{txn_hash}")
  

        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount entered.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SolanaWalletApp()
    window.show()
    sys.exit(app.exec())
