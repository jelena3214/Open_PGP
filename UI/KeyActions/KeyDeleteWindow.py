from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit


class KeyDeleteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Obriši ključ")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.text_input1 = QLineEdit(self)
        self.text_input1.setPlaceholderText("Unesite ID javnog ključa")

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(self.text_input1)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def on_confirm(self):
        first_text = self.text_input1.text()
        print(f"Uneti tekstovi su: {first_text}")
