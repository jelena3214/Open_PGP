from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit, QCheckBox, QHBoxLayout, QLabel

from KeyRings.KeyOperator import KeyOperator
from UI.ErrorDialog import show_error_message


class KeyImportWindow(QWidget):
    def __init__(self, parent, show_include_private_key_option):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Uvoz ključa")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

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
            "Upozorenje: Upamtite ovu novu šifru!"
        )
        passphrase_layout.addWidget(passphrase_label)
        passphrase_layout.addWidget(self.input_passphrase)

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

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
        filename = self.input_filename.text()
        if not filename:
            show_error_message("Naziv fajla je obavezno polje!")
            return
        include_private_key = self.include_private_key_checkbox.isChecked()

        if include_private_key:
            passphrase = self.input_passphrase.text()
            try:
                if not KeyOperator.import_key_set_from_pem(passphrase, filename):
                    show_error_message("Već postoji ključ ili par ključeva povezan sa ovim mejlom.")
                    return
            except:
                show_error_message("Ovaj fajl ne sadrži par ključeva u odgovarajućem formatu.")
                return
        else:
            try:
                name, _, _, _ = KeyOperator.import_public_key_from_pem(filename)
                if not name:
                    show_error_message("Već postoji ključ ili par ključeva povezan sa ovim mejlom.")
                    return
            except:
                show_error_message("Ovaj fajl ne sadrži javni ključ u odgovarajućem formatu.")
                return

        self.parent.refresh_window()
        self.close()
