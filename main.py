
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys
from solana_wallet import create_wallet, get_balance, send_transaction

class SolanaWalletUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 🌟 Window Properties
        self.setWindowTitle("Solana Wallet")
        self.setGeometry(100, 100, 400, 600)  # Mobile-like size
        self.setStyleSheet("""
            background-color: #F8F9FA;
            border-radius: 15px;
        """)

        # 🔹 Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 🎨 Header (Raleway)
        title = QLabel("Solana Wallet")
        title.setFont(QFont("Raleway", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #6A0DAD;")
        layout.addWidget(title)

        # 💰 Balance Display (Poppins)
        self.balance_label = QLabel("Balance: 0 SOL")
        self.balance_label.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balance_label.setStyleSheet("""
            color: #6A0DAD;
            padding: 10px;
            border-radius: 10px;
            background: linear-gradient(135deg, #E0BBE4, #957DAD);
        """)
        layout.addWidget(self.balance_label)

        # 📩 Address Input (Nunito)
        self.address_input = self.create_input("Enter Wallet Address", font="Nunito")
        layout.addWidget(self.address_input)

        # 🔄 Check Balance Button (Nunito)
        check_balance_btn = self.create_button("Check Balance", self.check_balance, "#6A0DAD", font="Nunito")
        layout.addWidget(check_balance_btn)

        # 📤 Send SOL Section (Work Sans)
        self.to_address_input = self.create_input("Recipient Address", font="Work Sans")
        layout.addWidget(self.to_address_input)

        self.amount_input = self.create_input("Amount (SOL)", font="Work Sans")
        layout.addWidget(self.amount_input)

        self.private_key_input = self.create_input("Enter Your Private Key", password=True, font="Work Sans")
        layout.addWidget(self.private_key_input)

        send_btn = self.create_button("Send SOL", self.send_sol, "#957DAD", font="Work Sans")
        layout.addWidget(send_btn)

        # 🆕 Create Wallet Button (Source Sans Pro)
        create_wallet_btn = self.create_button("Create New Wallet", self.create_wallet, "#D291BC", font="Source Sans Pro")
        layout.addWidget(create_wallet_btn)

        # 🚪 Exit Button (TT Neoris)
        exit_btn = self.create_button("Exit", self.close, "#FF3366", font="TT Neoris")
        layout.addWidget(exit_btn)

        # 🚀 Set Layout
        self.setLayout(layout)

    def create_input(self, placeholder, password=False, font="Nunito"):
        """Creates a modern input field with styling."""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFont(QFont(font, 14))
        if password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        input_field.setStyleSheet("""
            background-color: #FFFFFF; 
            color: #333333; 
            padding: 12px;
            border-radius: 10px;
            font-size: 14px;
            border: 2px solid #6A0DAD;
        """)
        return input_field

    def create_button(self, text, callback, color, font="Nunito"):
        """Creates a stylish button with hover effects."""
        btn = QPushButton(text)
        btn.setFont(QFont(font, 14, QFont.Weight.Bold))
        btn.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 12px;
            border-radius: 10px;
            border: none;
        """)
        btn.clicked.connect(callback)
        return btn

    def check_balance(self):
        address = self.address_input.text().strip()
        if not address:
            QMessageBox.warning(self, "Error", "Please enter a valid Solana address.")
            return
        balance = get_balance(address)
        self.balance_label.setText(f"Balance: {balance} SOL")

    def send_sol(self):
        private_key = self.private_key_input.text().strip()
        to_address = self.to_address_input.text().strip()
        amount_text = self.amount_input.text().strip()

        try:
            amount = float(amount_text)
            txn_hash = send_transaction(private_key, to_address, amount)
            QMessageBox.information(self, "Transaction Sent", f"Transaction Hash: {txn_hash}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount entered.")

    def create_wallet(self):
        wallet = create_wallet()
        QMessageBox.information(self, "Wallet Created", f"Address: {wallet['address']}\nPrivate Key: {wallet['private_key']}")

# 🎯 Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SolanaWalletUI()
    window.show()
    sys.exit(app.exec())
