import sys

from PyQt6.QtWidgets import QApplication

from KeyRings.PrivateKeyRing import PrivateKeyRing
from KeyRings.PublicKeyRing import PublicKeyRing
from Message import Message
from UI.MainMenuWindow import MainMenuWindow
import context

if __name__ == "__main__":
    context.private_key_ring = PrivateKeyRing()
    context.public_key_ring = PublicKeyRing()
    context.message = Message()
    app = QApplication(sys.argv)
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())
