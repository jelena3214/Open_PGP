import hashlib
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from Cryptodome.Cipher import CAST
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad


class PrivateKey:

    @classmethod
    def __init__(self, name, email, passphrase, public_key, private_key):
        self.timestamp = datetime.now()
        self.public_key = public_key
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        self.key_id = public_key_hex[-16:]
        self.name = name
        self.email = email

        passphrase_bytes = passphrase.encode('utf-8')
        sha1_hash = hashlib.sha1(passphrase_bytes).hexdigest()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        padded_private_key = pad(private_key_pem, 8)
        cipher = CAST.new(sha1_hash, CAST.MODE_ECB)
        self.encoded_private_key = cipher.encrypt(padded_private_key)

    @classmethod
    def decrypt_private_key(self, encrypted_private_key, passphrase):
        passphrase_bytes = passphrase.encode('utf-8')
        sha1_hash = hashlib.sha1(passphrase_bytes).hexdigest()

        cipher = CAST.new(sha1_hash, CAST.MODE_ECB)
        decrypted_private_key_padded = cipher.decrypt(encrypted_private_key)
        decrypted_private_key = unpad(decrypted_private_key_padded, 8)

        return decrypted_private_key

    def export_public_key_to_pem(self, public_key, file_path):
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(file_path, 'wb') as pem_file:
            pem_file.write(pem_data)

    def export_private_key_to_pem(self, private_key, file_path):
        pem_data_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(file_path, 'wb') as pem_file:
            pem_file.write(pem_data_private)

    def import_public_key_from_pem(self, file_path):
        with open(file_path, 'rb') as pem_file:
            pem_data = pem_file.read()

        public_key = serialization.load_pem_public_key(pem_data)

        return public_key

    #TODO: Should it be encrypted?
    def import_private_key_from_pem(self, file_path):
        with open(file_path, 'rb') as pem_file:
            pem_data = pem_file.read()

        private_key = serialization.load_pem_private_key(
            pem_data,
            password=None,
        )

        return private_key