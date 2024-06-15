from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit, QCheckBox, QHBoxLayout

from KeyRings.KeyOperator import KeyOperator
from UI.ErrorDialog import show_error_message
from UI.FileDialog import choose_import_file


class KeyImportWindow(QWidget):
    def __init__(self, parent, show_include_private_key_option):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Uvoz ključa")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

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

        layout.addLayout(file_input_layout)
        if show_include_private_key_option:
            layout.addWidget(self.include_private_key_checkbox)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def show_file_dialog(self):
        file_name = choose_import_file(self, "Uvoz ključa")
        self.input_filename.setText(file_name)

    def on_confirm(self):
        filename = self.input_filename.text()
        if not filename:
            show_error_message("Naziv fajla je obavezno polje!")
            return
        include_private_key = self.include_private_key_checkbox.isChecked()

        if include_private_key:
            try:
                if not KeyOperator.import_key_set_from_pem(filename):
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
