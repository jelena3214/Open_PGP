from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class PublicKey:

    def __init__(self, public_key, name, email, timestamp=None):
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.now()
        self.public_key = public_key
        self.email = email
        self.name = name
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.DER,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        self.key_id = public_key_hex[-16:]

    def public_key_as_string(self):
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return self.remove_pem_headers(public_key_pem.decode())

    @classmethod
    def string_to_public_key(cls, public_key_str):
        public_key_pem = f"-----BEGIN PUBLIC KEY-----\n{public_key_str}\n-----END PUBLIC KEY-----"
        return load_pem_public_key(public_key_pem.encode(), backend=default_backend())

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'public_key': self.public_key_as_string(),
            'email': self.email,
            'name': self.name,
            'key_id': self.key_id
        }

    @classmethod
    def from_dict(cls, data):
        public_key = cls.string_to_public_key(data['public_key'])
        timestamp = datetime.fromisoformat(data['timestamp'])
        return cls(public_key, data['name'], data['email'], timestamp)

    @classmethod
    def remove_pem_headers(cls, pem_key):
        lines = pem_key.strip().splitlines()
        pem_body = ''.join(line for line in lines if not (line.startswith('-----') and line.endswith('-----')))
        return pem_body
