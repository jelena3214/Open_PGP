import binascii
import hashlib
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from Cryptodome.Cipher import CAST
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad

from KeyRings.KeyOperator import KeyOperator


class PrivateKey:

    def __init__(self, name, email, passphrase, public_key, private_key):
        self.timestamp = datetime.now()
        self.public_key = public_key
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.DER,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        self.key_id = public_key_hex[-16:]
        self.name = name
        self.email = email

        passphrase_bytes = passphrase.encode('utf-8')
        sha1_hash = hashlib.sha1(passphrase_bytes).digest()
        cast_key = sha1_hash[:16]

        private_key_der = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        padded_private_key = pad(private_key_der, 8)
        cipher = CAST.new(cast_key, CAST.MODE_ECB)
        self.encoded_private_key = cipher.encrypt(padded_private_key)

    def public_key_as_string(self):
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return KeyOperator.remove_pem_headers(public_key_pem.decode())

    def private_key_as_string(self):
        return binascii.hexlify(self.encoded_private_key).decode('utf-8')

    @classmethod
    def decrypt_private_key(cls, encrypted_private_key, passphrase):
        passphrase_bytes = passphrase.encode('utf-8')
        sha1_hash = hashlib.sha1(passphrase_bytes).hexdigest()
        cast_key = sha1_hash[:16]
        cipher = CAST.new(cast_key, CAST.MODE_ECB)
        decrypted_private_key_padded = cipher.decrypt(encrypted_private_key)
        decrypted_private_key = unpad(decrypted_private_key_padded, 8)

        return decrypted_private_key
