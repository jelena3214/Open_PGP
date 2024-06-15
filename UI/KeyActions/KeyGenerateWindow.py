from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox

from AsymmetricEncription.RSAEncryption import RSAEncryption
import context
from UI.ErrorDialog import show_error_message


class KeyGenerateWindow(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Generisanje para ključeva")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Unesite ime")

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Unesite mejl")

        self.key_size_input = QComboBox(self)
        self.key_size_input.addItem("1024 bita")
        self.key_size_input.addItem("2048 bita")

        self.passphrase_input = QLineEdit(self)
        self.passphrase_input.setPlaceholderText("Unesite lozinku")
        self.passphrase_input.setEchoMode(QLineEdit.EchoMode.Password)
        passphrase_warning = QLabel(
            "Upozorenje: Upamtite ovu šifru!"
        )
        
        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(QLabel("Ime:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Mejl:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Veličina ključa:"))
        layout.addWidget(self.key_size_input)
        layout.addWidget(QLabel("Lozinka:"))
        layout.addWidget(self.passphrase_input)
        layout.addWidget(passphrase_warning)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def on_confirm(self):
        name = self.name_input.text()
        email = self.email_input.text()
        key_size = int(self.key_size_input.currentText().split()[0])
        passphrase = self.passphrase_input.text()

        public_key, private_key = RSAEncryption.generate_rsa_key_set(key_size)
        if not context.public_key_ring.add_new_public_key(name, email, public_key):
            show_error_message("Već postoji ključ ili par ključeva povezan sa ovim mejlom.")
            return

        context.private_key_ring.add_new_private_key(name, email, public_key, private_key, passphrase)

        self.parent.refresh_window()
        self.close()
