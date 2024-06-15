import os.path
import sys

from PyQt6.QtWidgets import QApplication

from KeyRings.PrivateKeyRing import PrivateKeyRing
from KeyRings.PublicKeyRing import PublicKeyRing
from Message import Message
from UI.MainMenuWindow import MainMenuWindow
import context

DATABASE_PUBLIC_KEYS = "data/init/database_public_keys"
DATABASE_PRIVATE_KEYS = "data/init/database_private_keys"


def export_all_keys():
    context.public_key_ring.export_all_public_keys(DATABASE_PUBLIC_KEYS)
    context.private_key_ring.export_all_private_keys(DATABASE_PRIVATE_KEYS)


def import_all_keys():
    if os.path.exists(DATABASE_PUBLIC_KEYS):
        context.public_key_ring.import_all_public_keys(DATABASE_PUBLIC_KEYS)
    if os.path.exists(DATABASE_PRIVATE_KEYS):
        context.private_key_ring.import_all_private_keys(DATABASE_PRIVATE_KEYS)


if __name__ == "__main__":
    context.private_key_ring = PrivateKeyRing()
    context.public_key_ring = PublicKeyRing()

    import_all_keys()

    context.message = Message()
    app = QApplication(sys.argv)

    app.aboutToQuit.connect(export_all_keys)

    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())
