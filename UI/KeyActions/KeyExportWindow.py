from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit, QCheckBox, QHBoxLayout

import context
from KeyRings.KeyOperator import KeyOperator
from UI.ErrorDialog import show_error_message
from UI.FileDialog import choose_export_file


class KeyExportWindow(QWidget):
    def __init__(self, show_include_private_key_option):
        super().__init__()
        self.setWindowTitle("Izvoz ključa")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.input_key_id = QLineEdit(self)
        self.input_key_id.setPlaceholderText("Unesite ID javnog ključa")

        file_input_layout = QHBoxLayout()

        self.input_filename = QLineEdit(self)
        self.input_filename.setPlaceholderText("Unesite ime fajla")
        file_input_layout.addWidget(self.input_filename)

        self.choose_file_button = QPushButton("Izaberite fajl")
        self.choose_file_button.clicked.connect(self.show_file_dialog)
        file_input_layout.addWidget(self.choose_file_button)

        self.include_private_key_checkbox = QCheckBox("Ceo set ključeva")

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(self.input_key_id)
        layout.addLayout(file_input_layout)
        if show_include_private_key_option:
            layout.addWidget(self.include_private_key_checkbox)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def show_file_dialog(self):
        file_name = choose_export_file(self, "Čuvanje ključa")
        self.input_filename.setText(file_name)

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
            KeyOperator.export_key_set_to_pem(private_key_struct, filename)
        else:
            public_key_struct = context.public_key_ring.get_key_by_key_id(key_id)

            if not public_key_struct:
                show_error_message("Za uneti ID ne postoji odgovarajući javni ključ!")
                return
            timestamp = public_key_struct.timestamp
            email = public_key_struct.email
            name = public_key_struct.name
            KeyOperator.export_public_key_to_pem(
                timestamp,
                email,
                name,
                public_key_struct.public_key,
                filename)

        self.close()
