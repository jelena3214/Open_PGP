from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel


class ReceiveMessageWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prijem poruke")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window

        # Layout za prozor 4
        layout = QVBoxLayout()

        # Primer sadržaja za prozor 4 (npr. tekstualni label)
        label = QLabel("Ovo je prozor 4")
        layout.addWidget(label)

        # Kreiranje dugmeta za povratak na meni
        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def back_to_main(self):
        self.main_window.show()
        self.close()