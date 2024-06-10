import hashlib
from datetime import datetime
from cryptography.hazmat.primitives import serialization

from KeyRings.KeyOperator import KeyOperator


class PublicKey:

    def __init__(self, public_key, name, email):
        self.timestamp = datetime.now()
        self.public_key = public_key
        self.email = email
        self.name = name
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.DER,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        self.key_id = public_key_hex[-16:]

    def public_key_to_string(self):
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return KeyOperator.remove_pem_headers(public_key_pem.decode())
