import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QLabel, QHeaderView, QLineEdit, QCheckBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meni Aplikacije")
        self.setGeometry(100, 100, 400, 300)

        button1 = QPushButton("Prsten javnih ključeva")
        button2 = QPushButton("Prsten privatnih ključeva")
        button3 = QPushButton("Slanje poruke")
        button4 = QPushButton("Prijem poruke")

        button1.clicked.connect(self.open_window1)
        button2.clicked.connect(self.open_window2)
        button3.clicked.connect(self.open_window3)
        button4.clicked.connect(self.open_window4)

        layout = QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_window1(self):
        self.new_window = Window1(self)
        self.new_window.show()
        self.close()

    def open_window2(self):
        self.new_window = Window2(self)
        self.new_window.show()
        self.close()

    def open_window3(self):
        self.new_window = Window3(self)
        self.new_window.show()
        self.close()

    def open_window4(self):
        self.new_window = Window4(self)
        self.new_window.show()
        self.close()


class Window1(QWidget):
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

        buttonA.clicked.connect(self.open_windowA)
        buttonB.clicked.connect(self.open_windowB)
        buttonC.clicked.connect(self.open_windowC)

        layout.addWidget(buttonA)
        layout.addWidget(buttonB)
        layout.addWidget(buttonC)

        back_button = QPushButton("Nazad na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_windowA(self):
        self.windowA = WindowA(False)
        self.windowA.show()

    def open_windowB(self):
        self.windowB = WindowB(False)
        self.windowB.show()

    def open_windowC(self):
        self.windowC = WindowC()
        self.windowC.show()

    def back_to_main(self):
        self.main_window.show()
        self.close()


class Window2(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prsten privatnih ključeva")
        self.setGeometry(100, 100, 900, 400)
        self.main_window = main_window

        layout = QVBoxLayout()

        data = [
            ["Podatak 1", "Podatak 2", "Podatak 3", "Podatak 4", "Podatak 5", "Podatak 6"],
            ["Podatak 7", "Podatak 8", "Podatak 9", "Podatak 10", "Podatak 11", "Podatak 12"],
            ["Podatak 13", "Podatak 14", "Podatak 15", "Podatak 16", "Podatak 17", "Podatak 18"],
        ]
        table = QTableWidget()
        table.setColumnCount(6)
        table.setRowCount(len(data))
        headers = ['Timestamp', 'KeyID', 'Public Key', 'Encripted Private Key', 'Name', 'Email']
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

        buttonA.clicked.connect(self.open_windowA)
        buttonB.clicked.connect(self.open_windowB)
        buttonC.clicked.connect(self.open_windowC)

        layout.addWidget(buttonA)
        layout.addWidget(buttonB)
        layout.addWidget(buttonC)

        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def open_windowA(self):
        self.windowA = WindowA(True)
        self.windowA.show()

    def open_windowB(self):
        self.windowB = WindowB(True)
        self.windowB.show()

    def open_windowC(self):
        self.windowC = WindowC()
        self.windowC.show()

    def back_to_main(self):
        self.main_window.show()
        self.close()


class Window3(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prozor 3")
        self.setGeometry(100, 100, 600, 400)
        self.main_window = main_window

        # Layout za prozor 3
        layout = QVBoxLayout()

        # Primer sadržaja za prozor 3 (npr. tekstualni label)
        label = QLabel("Ovo je prozor 3")
        layout.addWidget(label)

        # Kreiranje dugmeta za povratak na meni
        back_button = QPushButton("Vrati se na meni")
        back_button.clicked.connect(self.back_to_main)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def back_to_main(self):
        self.main_window.show()
        self.close()


class Window4(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Prozor 4")
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


class WindowA(QWidget):
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


class WindowB(QWidget):
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


class WindowC(QWidget):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
