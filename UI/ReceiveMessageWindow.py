import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDialog, \
    QMessageBox
from cryptography.exceptions import InvalidSignature

import context
from UI.ErrorDialog import show_error_message
from UI.FileDialog import choose_export_file, choose_import_file
from UI.KeyActions.PassphraseDialog import PassphraseDialog


class ReceiveMessageWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.print_string = None
        self.setWindowTitle("Prijem poruke")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window

        layout = QVBoxLayout()

        file_input_layout = QHBoxLayout()

        text_label = QLabel("Destinacija fajla:")
        layout.addWidget(text_label)

        self.input_filename = QLineEdit(self)
        self.input_filename.setPlaceholderText("Unesite ime fajla")
        file_input_layout.addWidget(self.input_filename)

        self.choose_file_button = QPushButton("Izaberite fajl")
        self.choose_file_button.clicked.connect(self.show_file_dialog)
        file_input_layout.addWidget(self.choose_file_button)
        layout.addLayout(file_input_layout)

        content_layout = QVBoxLayout()
        self.content_label = QLabel("Sadržaj:")
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        content_layout.addWidget(self.content_label)
        content_layout.addWidget(self.content_display)
        layout.addLayout(content_layout)

        buttons_layout = QHBoxLayout()
        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        buttons_layout.addWidget(back_button)

        display_button = QPushButton("Prikaži sadržaj")
        display_button.clicked.connect(self.display_content)
        buttons_layout.addWidget(display_button)

        self.save_button = QPushButton("Sačuvaj poruku")
        self.save_button.clicked.connect(self.save_message)
        self.save_button.setEnabled(False)
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def display_content(self):
        filepath = self.input_filename.text()
        if not os.path.exists(filepath):
            show_error_message("Fajl ne postoji!")
            return

        try:
            encrypted, receiver_private_key, msg, encrypted_ks_str, algo, comp, sign, encrypted, sender_email, receiver_email = context.message.get_passphase_for_receiving(
                filepath, context.private_key_ring)

            passphrase = None
            if encrypted:
                if receiver_private_key is None:
                    show_error_message("Ne postoji potreban ključ iz prstena privatnih ključeva za dekripciju poruke!")
                    return
                passphrase_dialog = PassphraseDialog(receiver_email)
                if passphrase_dialog.exec() == QDialog.DialogCode.Accepted:
                    passphrase = passphrase_dialog.get_passphrase()

            message_str = context.message.receive_message(msg, passphrase, receiver_private_key, encrypted_ks_str,
                                                          context.public_key_ring, algo, comp, sign, encrypted)
        except InvalidSignature:
            show_error_message("Potpis poruke nije validan!")
            return
        except BaseException as e:
            show_error_message(f"Sadržaj poruke je izmenjen! (Exception: {'{} - {}'.format(type(e).__name__, str(e))})")
            return

        self.print_string = f"From:{sender_email}\nTo:{receiver_email}\n{message_str}"

        self.content_display.setPlainText(self.print_string)
        self.save_button.setEnabled(True)

    def show_file_dialog(self):
        file_name = choose_import_file(self, "Primanje poruke")
        self.input_filename.setText(file_name)

    def save_message(self):
        fileName = choose_export_file(self, "Čuvanje poruke")
        if fileName:
            try:
                with open(fileName, 'w') as file:
                    file.write(self.print_string)
                QMessageBox.information(self, "Uspeh", f"Poruka sačuvana na putanji {fileName}")
            except Exception as e:
                QMessageBox.critical(self, "Greška", f"Greška pri čuvanju poruke: {e}")

    def back_to_main(self):
        self.main_window.show()
        self.close()
