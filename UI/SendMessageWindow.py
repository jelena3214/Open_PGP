from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QCheckBox, QRadioButton, QHBoxLayout, QMessageBox

import context
from UI.ErrorDialog import show_error_message


class SendMessageWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Slanje poruke")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window

        layout = QVBoxLayout()

        text_layout = QHBoxLayout()
        text_label = QLabel("Vaš email:")
        self.text_input_signer = QLineEdit()
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input_signer)

        layout.addLayout(text_layout)

        text_layout = QHBoxLayout()
        text_label = QLabel("Email primaoca:")
        self.text_input = QLineEdit()
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input)

        layout.addLayout(text_layout)

        self.checkbox_sign = QCheckBox("Potpisivanje poruke")
        self.checkbox_sign.stateChanged.connect(self.toggle_fields_signature)
        layout.addWidget(self.checkbox_sign)

        text_layout = QHBoxLayout()
        text_label = QLabel("Šifra tajnog ključa:")
        self.text_input_pass = QLineEdit()
        self.text_input_pass.setEnabled(False)
        self.text_input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input_pass)

        layout.addLayout(text_layout)

        self.checkbox = QCheckBox("Šifrovanje poruke")
        self.checkbox.stateChanged.connect(self.toggle_fields)
        layout.addWidget(self.checkbox)

        self.radio_button1 = QRadioButton("Triple DES")
        self.radio_button1.setEnabled(False)
        layout.addWidget(self.radio_button1)

        self.radio_button2 = QRadioButton("AES 128")
        self.radio_button2.setEnabled(False)
        layout.addWidget(self.radio_button2)

        self.checkbox_comp = QCheckBox("Kompresija poruke")
        layout.addWidget(self.checkbox_comp)

        self.checkbox_radix64 = QCheckBox("Radix64 konverzija poruke")
        layout.addWidget(self.checkbox_radix64)

        text_layout = QHBoxLayout()
        text_label = QLabel("Poruka:")
        self.text_input_message = QLineEdit()
        self.text_input_message.setFixedWidth(600)
        self.text_input_message.setFixedHeight(100)
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input_message)

        layout.addLayout(text_layout)

        text_layout = QHBoxLayout()
        text_label = QLabel("Destinacija fajla:")
        self.text_input_filepath = QLineEdit()
        text_layout.addWidget(text_label)
        text_layout.addWidget(self.text_input_filepath)

        layout.addLayout(text_layout)

        submit_button = QPushButton("Pošalji")
        submit_button.clicked.connect(self.send_message)
        layout.addWidget(submit_button)

        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def toggle_fields(self):
        state = self.checkbox.isChecked()
        self.radio_button1.setEnabled(state)
        self.radio_button2.setEnabled(state)

    def toggle_fields_signature(self):
        state = self.checkbox_sign.isChecked()
        self.text_input_pass.setEnabled(state)

    def back_to_main(self):
        self.main_window.show()
        self.close()

    def send_message(self):
        filepath = self.text_input_filepath.text()
        selected_algo = ""
        msg = self.text_input_message.text()
        signature = self.checkbox_sign.isChecked()
        signer_email = self.text_input_signer.text()
        receiver_email = self.text_input.text()
        encryption = self.checkbox.isChecked()
        compressed = self.checkbox_comp.isChecked()
        radix64 = self.checkbox_radix64.isChecked()
        private_key_sender = None
        sender_private_key = None
        public_key_receiver = None

        if signature:
            passphrase = self.text_input_pass.text()
            private_key_sender = context.private_key_ring.get_key_by_email(signer_email)
            # ne postoji taj email
            if not private_key_sender:
                show_error_message("Za uneti email ne postoji odgovarajući ključ!")
                return
            sender_private_key = private_key_sender.decrypt_private_key(passphrase)

        if encryption:
            selected_algo = self.get_selected_radio()

            public_key_receiver = context.public_key_ring.get_key_by_email(receiver_email)

        context.message.send_message(signature, encryption, compressed, radix64, selected_algo, signer_email, receiver_email,
                             msg, sender_private_key, private_key_sender, public_key_receiver, filepath)

    # If none is checked default is TripleDES
    def get_selected_radio(self):
        if self.radio_button1.isChecked():
            return "TripleDES"
        elif self.radio_button2.isChecked():
            return "AES128"
        else:
            return "Nijedan"
