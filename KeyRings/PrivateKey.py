import hashlib
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from Cryptodome.Cipher import CAST
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad


class PrivateKey:

    @classmethod
    def __init__(cls, name, email, passphrase, public_key, private_key):
        cls.timestamp = datetime.now()
        cls.public_key = public_key
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        cls.key_id = public_key_hex[-16:]
        cls.name = name
        cls.email = email

        passphrase_bytes = passphrase.encode('utf-8')
        sha1_hash = hashlib.sha1(passphrase_bytes).hexdigest()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        padded_private_key = pad(private_key_pem, 8)
        cipher = CAST.new(sha1_hash, CAST.MODE_ECB)
        cls.encoded_private_key = cipher.encrypt(padded_private_key)

    @classmethod
    def decrypt_private_key(self, encrypted_private_key, passphrase):
        passphrase_bytes = passphrase.encode('utf-8')
        sha1_hash = hashlib.sha1(passphrase_bytes).hexdigest()

        cipher = CAST.new(sha1_hash, CAST.MODE_ECB)
        decrypted_private_key_padded = cipher.decrypt(encrypted_private_key)
        decrypted_private_key = unpad(decrypted_private_key_padded, 8)

        return decrypted_private_key
