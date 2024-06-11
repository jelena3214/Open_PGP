from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QLabel, QHBoxLayout

from UI.KeyActions.KeyDeleteWindow import KeyDeleteWindow
from UI.KeyActions.KeyExportWindow import KeyExportWindow
from UI.KeyActions.KeyImportWindow import KeyImportWindow
from UI.KeyActions.KeyTableUtils import initTable, updatePublicRingTable
import context


class PublicKeyRingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.key_delete_window = None
        self.key_export_window = None
        self.key_import_window = None
        self.main_window = main_window

        self.setWindowTitle("Prsten javnih ključeva")
        self.setGeometry(100, 100, 600, 400)
        self.headers = ['Timestamp', 'KeyID', 'Public Key', 'Name', 'Email']

        layout = QVBoxLayout()

        num_of_public_ring_keys = len(context.public_key_ring.public_keys)

        if num_of_public_ring_keys:
            self.table = QTableWidget()
            initTable(self.table, column_count=len(self.headers), row_count=num_of_public_ring_keys,
                      headers=self.headers)
            updatePublicRingTable(self.table)
            layout.addWidget(self.table)
        else:
            hbox = QHBoxLayout()
            label = QLabel("Nema javnih ključeva")
            hbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addLayout(hbox)

        button1 = QPushButton("Uvezi javni ključ")
        button2 = QPushButton("Izvezi javni ključ")
        button3 = QPushButton("Obriši ključ")

        button1.clicked.connect(self.open_key_import)
        button2.clicked.connect(self.open_key_export)
        button3.clicked.connect(self.open_key_delete)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        back_button = QPushButton("Nazad na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_key_import(self):
        self.key_import_window = KeyImportWindow(False)
        self.key_import_window.show()

    def open_key_export(self):
        self.key_export_window = KeyExportWindow(False)
        self.key_export_window.show()

    def open_key_delete(self):
        self.key_delete_window = KeyDeleteWindow()
        self.key_delete_window.show()

    def back_to_main(self):
        self.main_window.show()
        self.close()
