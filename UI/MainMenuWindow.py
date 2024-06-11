from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from UI.PrivateKeyRingWindow import PrivateKeyRingWindow
from UI.PublicKeyRingWindow import PublicKeyRingWindow
from UI.ReceiveMessageWindow import ReceiveMessageWindow
from UI.SendMessageWindow import SendMessageWindow


class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.subWindow = None
        self.setWindowTitle("Meni Aplikacije")
        self.setGeometry(100, 100, 400, 300)

        button1 = QPushButton("Prsten javnih ključeva")
        button2 = QPushButton("Prsten privatnih ključeva")
        button3 = QPushButton("Slanje poruke")
        button4 = QPushButton("Prijem poruke")

        button1.clicked.connect(self.open_public_key_ring)
        button2.clicked.connect(self.open_private_key_ring)
        button3.clicked.connect(self.open_send_message)
        button4.clicked.connect(self.open_receive_message)

        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_public_key_ring(self):
        self.subWindow = PublicKeyRingWindow(self)
        self.subWindow.show()
        self.close()

    def open_private_key_ring(self):
        self.subWindow = PrivateKeyRingWindow(self)
        self.subWindow.show()
        self.close()

    def open_send_message(self):
        self.subWindow = SendMessageWindow(self)
        self.subWindow.show()
        self.close()

    def open_receive_message(self):
        self.subWindow = ReceiveMessageWindow(self)
        self.subWindow.show()
        self.close()
