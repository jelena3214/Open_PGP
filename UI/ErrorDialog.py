from PyQt6.QtWidgets import QMessageBox


def show_error_message(message):
    error_dialog = QMessageBox()
    error_dialog.setIcon(QMessageBox.Icon.Critical)
    error_dialog.setWindowTitle("Greška")
    error_dialog.setText(message)
    error_dialog.exec()
