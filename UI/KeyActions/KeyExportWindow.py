from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit, QCheckBox, QHBoxLayout, QLabel

from KeyRings.KeyOperator import KeyOperator
import context
from UI.ErrorDialog import show_error_message


class KeyExportWindow(QWidget):
    def __init__(self, show_include_private_key_option):
        super().__init__()
        self.setWindowTitle("Izvoz ključa")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.input_key_id = QLineEdit(self)
        self.input_key_id.setPlaceholderText("Unesite ID javnog ključa")
        self.input_filename = QLineEdit(self)
        self.input_filename.setPlaceholderText("Unesite ime fajla")

        self.include_private_key_checkbox = QCheckBox("Ceo set ključeva")
        self.include_private_key_checkbox.stateChanged.connect(self.toggle_passphrase_field)

        passphrase_layout = QHBoxLayout()
        passphrase_label = QLabel("Šifra tajnog ključa:")
        self.input_passphrase = QLineEdit()
        self.input_passphrase.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_passphrase.setEnabled(False)
        passphrase_warning = QLabel(
            "Upozorenje: pogrešna šifra rezultovaće potencijalno u nepopravljivo pogrešnom privatnom ključu."
        )
        passphrase_layout.addWidget(passphrase_label)
        passphrase_layout.addWidget(self.input_passphrase)

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(self.input_key_id)
        layout.addWidget(self.input_filename)
        if show_include_private_key_option:
            layout.addWidget(self.include_private_key_checkbox)
            layout.addLayout(passphrase_layout)
            layout.addWidget(passphrase_warning)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def toggle_passphrase_field(self):
        state = self.include_private_key_checkbox.isChecked()
        self.input_passphrase.setEnabled(state)

    def on_confirm(self):
        key_id = self.input_key_id.text()
        filename = self.input_filename.text()
        if not key_id or not filename:
            show_error_message("Polja ID i naziv fajla su obavezna!")
            return
        include_private_key = self.include_private_key_checkbox.isChecked()

        if include_private_key:
            private_key_struct = context.private_key_ring.get_key_by_key_id(key_id)

            if not private_key_struct:
                show_error_message(
                    "Za uneti ID ne postoji odgovarajući privatni ključ!\n"
                    "Za izvoz tuđeg javnog ključa isključite opciju \"Ceo set ključeva\"."
                )
                return
            passphrase = self.input_passphrase.text()
            if not KeyOperator.export_key_set_to_pem(
                    private_key_struct,
                    passphrase,
                    filename):
                show_error_message("Neuspešan izvoz, problem sa šifrom!")
                return
        else:
            public_key_struct = context.public_key_ring.get_key_by_key_id(key_id)

            if not public_key_struct:
                show_error_message("Za uneti ID ne postoji odgovarajući javni ključ!")
                return
            timestamp = public_key_struct.timestamp
            email = public_key_struct.email
            name = public_key_struct.name
            key_id = public_key_struct.key_id
            KeyOperator.export_public_key_to_pem(
                timestamp,
                email,
                name,
                key_id,
                public_key_struct.public_key,
                filename)

        self.close()
