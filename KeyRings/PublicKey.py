import hashlib
from datetime import datetime
from cryptography.hazmat.primitives import serialization


class PublicKey:
    @classmethod
    def __init__(cls, public_key, name, email):
        cls.timestamp = datetime.now()
        cls.public_key = public_key
        cls.email = email
        cls.name = name
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        cls.key_id = public_key_hex[-16:]
