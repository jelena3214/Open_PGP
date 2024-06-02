from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


class AES128:
    def __init__(self):
        self.iv = b'0123456789101112'

    def encrypt_cfb64(self, plaintext, key):
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CFB(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        return ciphertext

    def decrypt_cfb64(self, ciphertext, key):
        cipher = Cipher(algorithms.AES(key), modes.CFB(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext


# Primer korišćenja:
key = os.urandom(16)  # AES-128 zahteva ključ od 16 bajtova (128 bita)

plaintext = b"Ovo je testna poruka."
a = AES128()
# Šifrovanje
ciphertext = a.encrypt_cfb64(plaintext, key)
print("Šifrovana poruka (ciphertext):", ciphertext)

# Dešifrovanje
decrypted_plaintext = a.decrypt_cfb64(ciphertext, key)
print("Dešifrovana poruka:", decrypted_plaintext.decode('utf-8'))
