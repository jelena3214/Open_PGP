from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLineEdit, QCheckBox


class KeyImportWindow(QWidget):
    def __init__(self, show_checkbox_label):
        super().__init__()
        self.setWindowTitle("Uvoz ključa")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.text_input1 = QLineEdit(self)
        self.text_input1.setPlaceholderText("Unesite ID javnog ključa")
        self.text_input2 = QLineEdit(self)
        self.text_input2.setPlaceholderText("Unesite ime fajla")

        self.checkbox = QCheckBox("Ceo set ključeva")

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(self.text_input1)
        layout.addWidget(self.text_input2)
        if show_checkbox_label: layout.addWidget(self.checkbox)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def on_confirm(self):
        first_text = self.text_input1.text()
        second_text = self.text_input2.text()
        checkbox = self.checkbox.isChecked()
        print(f"Uneti tekstovi su: {first_text} i {second_text} i {checkbox}")

