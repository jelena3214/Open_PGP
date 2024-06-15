from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit

import context
from UI.ErrorDialog import show_error_message


class KeyDeleteWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Brisanje ključeva")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.input_key_id = QLineEdit(self)
        self.input_key_id.setPlaceholderText("Unesite ID javnog ključa")

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(self.input_key_id)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def on_confirm(self):
        key_id = self.input_key_id.text()
        if not context.public_key_ring.delete_public_key(key_id):
            show_error_message("Ne postoji javni ključ sa traženim ID.")
            return
        else:
            context.private_key_ring.delete_private_key(key_id)

        self.parent.refresh_window()
        self.close()
