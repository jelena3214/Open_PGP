from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QLabel, QHBoxLayout

from AsymmetricEncription.RSAEncryption import RSAEncryption
from UI.KeyActions.KeyDeleteWindow import KeyDeleteWindow
from UI.KeyActions.KeyExportWindow import KeyExportWindow
from UI.KeyActions.KeyGenerateWindow import KeyGenerateWindow
from UI.KeyActions.KeyImportWindow import KeyImportWindow
from UI.KeyActions.KeyTableUtils import initTable, updatePrivateRingTable
import context


class PrivateKeyRingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.key_generate_window = None
        self.key_delete_window = None
        self.key_export_window = None
        self.key_import_window = None
        self.main_window = main_window

        self.setWindowTitle("Prsten privatnih ključeva")
        self.setGeometry(100, 100, 900, 400)
        self.headers = ['Timestamp', 'KeyID', 'Public Key', 'Encripted Private Key', 'Name', 'Email']

        public_key, private_key = RSAEncryption.generate_rsa_key_set(1024)
        context.private_key_ring.add_new_private_key("lol", "lol", public_key, private_key, "123")

        layout = QVBoxLayout()

        num_of_private_ring_keys = len(context.private_key_ring.private_keys)

        if num_of_private_ring_keys:
            self.table = QTableWidget()
            initTable(self.table, column_count=len(self.headers), row_count=num_of_private_ring_keys, headers=self.headers)
            updatePrivateRingTable(self.table)
            layout.addWidget(self.table)
        else:
            hbox = QHBoxLayout()
            label = QLabel("Nema privatnih ključeva")
            hbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addLayout(hbox)

        button1 = QPushButton("Uvezi par ključeva")
        button2 = QPushButton("Izvezi par ključeva")
        button3 = QPushButton("Obriši par ključeva")
        button4 = QPushButton("Generiši par ključeva")

        button1.clicked.connect(self.open_key_import)
        button2.clicked.connect(self.open_key_export)
        button3.clicked.connect(self.open_key_delete)
        button4.clicked.connect(self.open_key_generate)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)

        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_key_import(self):
        self.key_import_window = KeyImportWindow(True)
        self.key_import_window.show()

    def open_key_export(self):
        self.key_export_window = KeyExportWindow(True)
        self.key_export_window.show()

    def open_key_delete(self):
        self.key_delete_window = KeyDeleteWindow()
        self.key_delete_window.show()

    def open_key_generate(self):
        self.key_generate_window = KeyGenerateWindow(self)
        self.key_generate_window.show()

    def back_to_main(self):
        self.main_window.show()
        self.close()

    def refresh_window(self):
        updatePrivateRingTable(self.table)
