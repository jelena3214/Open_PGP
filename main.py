import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QLabel, QHeaderView, QLineEdit, QCheckBox, QRadioButton, QHBoxLayout, QMessageBox, QComboBox

from KeyRings.PrivateKeyRing import PrivateKeyRing
from KeyRings.PublicKeyRing import PublicKeyRing
from Message import Message
from AsymmetricEncription.RSAEncryption import RSAEncryption


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.new_window = PublicKeyRingWindow(self)
        self.new_window.show()
        self.close()

    def open_private_key_ring(self):
        self.new_window = PrivateKeyRingWindow(self)
        self.new_window.show()
        self.close()

    def open_send_message(self):
        self.new_window = SendMessageWindow(self)
        self.new_window.show()
        self.close()

    def open_receive_message(self):
        self.new_window = ReceiveMessageWindow(self)
        self.new_window.show()
        self.close()


class PublicKeyRingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prsten javnih ključeva")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window

        layout = QVBoxLayout()

        data = [
            ["Podatak 1", "Podatak 2", "Podatak 3", "Podatak 4", "Podatak 5"],
            ["Podatak 6", "Podatak 7", "Podatak 8", "Podatak 9", "Podatak 10"],
            ["Podatak 11", "Podatak 12", "Podatak 13", "Podatak 14", "Podatak 15"],
        ]
        table = QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(len(data))
        headers = ['Timestamp', 'KeyID', 'Public Key', 'Name', 'Email']
        table.setHorizontalHeaderLabels(headers)

        header = table.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            item = table.horizontalHeaderItem(i)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(cell_data))

        layout.addWidget(table)

        buttonA = QPushButton("Uvezi ključ")
        buttonB = QPushButton("Izvezi ključ")
        buttonC = QPushButton("Obriši ključ")

        buttonA.clicked.connect(self.open_key_import)
        buttonB.clicked.connect(self.open_key_export)
        buttonC.clicked.connect(self.open_delete_key)

        layout.addWidget(buttonA)
        layout.addWidget(buttonB)
        layout.addWidget(buttonC)

        back_button = QPushButton("Nazad na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_key_import(self):
        self.windowA = KeyImportWindow(False)
        self.windowA.show()

    def open_key_export(self):
        self.windowB = KeyExportWindow(False)
        self.windowB.show()

    def open_delete_key(self):
        self.windowC = DeleteKeyWindow()
        self.windowC.show()

    def back_to_main(self):
        self.main_window.show()
        self.close()


def initTable(table):
    table.setColumnCount(6)
    table.setRowCount(len(private_key_ring.private_keys))
    headers = ['Timestamp', 'KeyID', 'Public Key', 'Encripted Private Key', 'Name', 'Email']
    table.setHorizontalHeaderLabels(headers)

    header = table.horizontalHeader()
    for i in range(len(headers)):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        item = table.horizontalHeaderItem(i)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)


def updateTable(table):
    table.clearContents()
    all_data = private_key_ring.get_all_data()
    table.setRowCount(len(all_data))
    for row_idx in range(len(all_data)):
        private_key = all_data[row_idx]
        print(private_key.name)
        table.setItem(row_idx, 0, QTableWidgetItem(str(private_key.timestamp)))
        table.setItem(row_idx, 1, QTableWidgetItem(private_key.key_id))
        table.setItem(row_idx, 2, QTableWidgetItem(str(private_key.public_key_as_string())))
        table.setItem(row_idx, 3, QTableWidgetItem(str(private_key.private_key_as_string())))
        table.setItem(row_idx, 4, QTableWidgetItem(private_key.name))
        table.setItem(row_idx, 5, QTableWidgetItem(private_key.email))

    # for row_idx, private_key in enumerate(private_key_ring.get_all_data()):
    #     print("str ovde" + private_key.name)
    #     table.setItem(row_idx, 0, QTableWidgetItem(str(private_key.timestamp)))
    #     table.setItem(row_idx, 1, QTableWidgetItem(private_key.key_id))
    #     table.setItem(row_idx, 2, QTableWidgetItem(str(private_key.public_key_as_string())))
    #     table.setItem(row_idx, 3, QTableWidgetItem(str(private_key.private_key_as_string())))
    #     table.setItem(row_idx, 4, QTableWidgetItem(private_key.name))
    #     table.setItem(row_idx, 5, QTableWidgetItem(private_key.email))


class PrivateKeyRingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prsten privatnih ključeva")
        self.setGeometry(100, 100, 900, 400)
        self.main_window = main_window

        public_key, private_key = RSAEncryption.generate_rsa_key_set(1024)
        private_key_ring.add_new_private_key("lol", "lol", public_key, private_key, "123")
        layout = QVBoxLayout()

        if len(private_key_ring.private_keys):
            self.table = QTableWidget()
            initTable(self.table)
            updateTable(self.table)
            layout.addWidget(self.table)
        else:
            hbox = QHBoxLayout()
            label = QLabel("Nema privatnih ključeva")
            hbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addLayout(hbox)
        buttonA = QPushButton("Uvezi ključ")
        buttonB = QPushButton("Izvezi ključ")
        buttonC = QPushButton("Obriši ključ")
        buttonD = QPushButton("Generiši ključ")

        buttonA.clicked.connect(self.open_key_import)
        buttonB.clicked.connect(self.open_key_export)
        buttonC.clicked.connect(self.open_delete_key)
        buttonD.clicked.connect(self.open_key_generate)

        layout.addWidget(buttonA)
        layout.addWidget(buttonB)
        layout.addWidget(buttonC)
        layout.addWidget(buttonD)

        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_key_import(self):
        self.windowA = KeyImportWindow(True)
        self.windowA.show()

    def open_key_export(self):
        self.windowB = KeyExportWindow(True)
        self.windowB.show()

    def open_delete_key(self):
        self.windowC = DeleteKeyWindow()
        self.windowC.show()

    def open_key_generate(self):
        self.windowD = KeyGenerateWindow(self)
        self.windowD.show()

    def back_to_main(self):
        self.main_window.show()
        self.close()

    def refresh_window(self):
        updateTable(self.table)


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
        text_label = QLabel("Passphase:")
        self.text_input_pass = QLineEdit()
        self.text_input_pass.setEnabled(False)
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
        message = self.text_input_message.text()
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
            passphase = self.text_input_pass.text()
            private_key_sender = private_key_ring.get_key_by_email(signer_email)
            # ne postoji taj email
            if not private_key_sender:
                self.show_error_message("Za uneti email ne postoji odgovarajući ključ!")
                return
            sender_private_key = private_key_sender.decrypt_private_key(private_key_sender.encoded_private_key, passphase)

        if encryption:
            selected_algo = self.get_selected_radio()

            public_key_receiver = public_key_ring.get_key_by_email(receiver_email)

        message.send_message(signature, encryption, compressed, radix64, selected_algo, message, sender_private_key,
                             private_key_sender.key_id, public_key_receiver, public_key_receiver.key_id, filepath)

    # If none is checked default is TripleDES
    def get_selected_radio(self):
        if self.radio_button1.isChecked():
            return "TripleDES"
        elif self.radio_button2.isChecked():
            return "AES128"
        else:
            return "Nijedan"

    def show_error_message(self, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Greška")
        error_dialog.setText(message)
        error_dialog.exec()


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


class KeyExportWindow(QWidget):
    def __init__(self, show_checkbox_label):
        super().__init__()
        self.setWindowTitle("Izvoz ključa")
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


class DeleteKeyWindow(QWidget):
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


class KeyGenerateWindow(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Generiši par ključeva")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Unesite ime")

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Unesite mejl")

        self.key_size_input = QComboBox(self)
        self.key_size_input.addItem("1024 bita")
        self.key_size_input.addItem("2048 bita")

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Unesite lozinku")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_button = QPushButton("Potvrdi", self)
        self.confirm_button.clicked.connect(self.on_confirm)

        layout.addWidget(QLabel("Ime:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Mejl:"))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel("Veličina ključa:"))
        layout.addWidget(self.key_size_input)
        layout.addWidget(QLabel("Lozinka:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def on_confirm(self):
        name = self.name_input.text()
        email = self.email_input.text()
        key_size = int(self.key_size_input.currentText().split()[0])
        passphrase = self.password_input.text()
        print(f"Uneti podaci su: Ime: {name}, Mejl: {email}, Veličina ključa: {key_size}, Lozinka: {passphrase}")

        public_key, private_key = RSAEncryption.generate_rsa_key_set(key_size)
        print(public_key, private_key)
        private_key_ring.add_new_private_key(name, email, public_key, private_key, passphrase)
        public_key_ring.add_new_public_key(name, email, public_key)
        print(private_key_ring.get_all_data())
        print(f"Uneti podaci su: Ime: {name}, Mejl: {email}, Veličina ključa: {key_size}, Lozinka: {passphrase}")
        self.parent.refresh_window()
        self.close()


if __name__ == "__main__":
    private_key_ring = PrivateKeyRing()
    public_key_ring = PublicKeyRing()
    message = Message()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
