from PyQt6.QtWidgets import (
    QVBoxLayout, QLineEdit, QDialog, QDialogButtonBox, QFormLayout
)


class PassphraseDialog(QDialog):
    def __init__(self, email):
        super().__init__()
        self.setWindowTitle("Unesite šifru")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.form_layout = QFormLayout()
        self.passphrase_input = QLineEdit()
        self.passphrase_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.form_layout.addRow(f"Šifra za email {email}:", self.passphrase_input)

        self.layout.addLayout(self.form_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    def get_passphrase(self):
        return self.passphrase_input.text()