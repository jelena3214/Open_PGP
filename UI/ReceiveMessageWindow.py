import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDialog
from cryptography.exceptions import InvalidSignature

import context
from UI.KeyActions.PassphraseDialog import PassphraseDialog
from UI.ErrorDialog import show_error_message


class ReceiveMessageWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prijem poruke")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window

        layout = QVBoxLayout()

        text_layout = QHBoxLayout()
        text_label = QLabel("Destinacija fajla:")
        self.text_input_filepath = QLineEdit()
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input_filepath)
        layout.addLayout(text_layout)

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

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def display_content(self):
        filepath = self.text_input_filepath.text()
        if not os.path.exists(filepath):
            show_error_message("Fajl ne postoji!")
            return

        try:
            encrypted, receiver_private_key, msg, encrypted_ks_str, algo, comp, sign, encrypted, sender_email, receiver_email = context.message.get_passphase_for_receiving(
                filepath, context.private_key_ring)


            passphrase = None
            if encrypted:
                if receiver_private_key is None:
                    show_error_message("Ne postoji potreban ključ iz prstena privatnih ključeva!")
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

        print_string = f"From:{sender_email}\nTo:{receiver_email}\n{message_str}"

        self.content_display.setPlainText(print_string)

    def back_to_main(self):
        self.main_window.show()
        self.close()
