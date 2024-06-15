from PyQt6.QtWidgets import QFileDialog


def choose_export_file(parent, dialog_title):
    fileName, _ = QFileDialog.getSaveFileName(parent, dialog_title, "", "Text Files (*.txt);;All Files (*)")
    return fileName


def choose_import_file(parent, dialog_title):
    fileName, _ = QFileDialog.getOpenFileName(parent, dialog_title, "", "Text Files (*.txt);;All Files (*)")
    return fileName
