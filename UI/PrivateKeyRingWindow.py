from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QTableWidget, QLabel, QStackedWidget, QApplication

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

        layout = QVBoxLayout()

        num_of_private_ring_keys = len(context.private_key_ring.private_keys)

        self.stacked_widget = QStackedWidget()

        table_widget = QWidget()
        table_layout = QVBoxLayout()
        self.table = QTableWidget()
        initTable(self.table, column_count=len(self.headers), row_count=num_of_private_ring_keys, headers=self.headers)
        updatePrivateRingTable(self.table)
        table_layout.addWidget(self.table)
        table_widget.setLayout(table_layout)

        empty_message_widget = QWidget()
        empty_layout = QVBoxLayout()
        label = QLabel("Nema privatnih ključeva")
        empty_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        empty_message_widget.setLayout(empty_layout)

        self.stacked_widget.addWidget(table_widget)
        self.stacked_widget.addWidget(empty_message_widget)

        layout.addWidget(self.stacked_widget)
        if not num_of_private_ring_keys:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)

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

        self.closing_by_button = True

        self.setLayout(layout)

    def open_key_import(self):
        self.key_import_window = KeyImportWindow(parent=self, show_include_private_key_option=True)
        self.key_import_window.show()

    def open_key_export(self):
        self.key_export_window = KeyExportWindow(show_include_private_key_option=True)
        self.key_export_window.show()

    def open_key_delete(self):
        self.key_delete_window = KeyDeleteWindow(parent=self)
        self.key_delete_window.show()

    def open_key_generate(self):
        self.key_generate_window = KeyGenerateWindow(parent=self)
        self.key_generate_window.show()

    def back_to_main(self):
        self.closing_by_button = True
        self.main_window.show()
        self.close()

    def refresh_window(self):
        if not len(context.private_key_ring.private_keys):
            self.stacked_widget.setCurrentIndex(1)
        else:
            updatePrivateRingTable(self.table)
            self.stacked_widget.setCurrentIndex(0)

    def closeEvent(self, event):
        if not self.closing_by_button:
            QApplication.quit()
        else:
            event.accept()
