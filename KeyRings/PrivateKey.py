import binascii
import hashlib
from datetime import datetime

from Cryptodome.Cipher import CAST
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key


class PrivateKey:

    def __init__(self, name, email, passphrase, public_key, private_key, timestamp=None):
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.now()
        self.public_key = public_key
        public_key_hex = public_key.public_bytes(encoding=serialization.Encoding.DER,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo).hex()
        self.key_id = public_key_hex[-16:]
        self.name = name
        self.email = email

        if passphrase:
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
        else:
            self.encoded_private_key = private_key

    def public_key_as_string(self):
        public_key_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return self.remove_pem_headers(public_key_pem.decode())

    def private_key_as_string(self):
        return binascii.hexlify(self.encoded_private_key).decode('utf-8')

    @classmethod
    def string_to_public_key(cls, public_key_str):
        public_key_pem = f"-----BEGIN PUBLIC KEY-----\n{public_key_str}\n-----END PUBLIC KEY-----"
        return load_pem_public_key(public_key_pem.encode(), backend=default_backend())

    @classmethod
    def string_to_private_key(cls, private_key_str):
        return binascii.unhexlify(private_key_str)

    def decrypt_private_key(self, passphrase):
        try:
            passphrase_bytes = passphrase.encode('utf-8')
            sha1_hash = hashlib.sha1(passphrase_bytes).digest()
            cast_key = sha1_hash[:16]
            cipher = CAST.new(cast_key, CAST.MODE_ECB)
            decrypted_private_key_padded = cipher.decrypt(self.encoded_private_key)
            decrypted_private_key_der = unpad(decrypted_private_key_padded, 8)

            return serialization.load_der_private_key(
                data=decrypted_private_key_der,
                password=None
            )
        except:
            return None

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'public_key': self.public_key_as_string(),
            'encoded_private_key': self.private_key_as_string(),
            'email': self.email,
            'name': self.name,
            'key_id': self.key_id
        }

    @classmethod
    def from_dict(cls, data):
        public_key = cls.string_to_public_key(data['public_key'])
        private_key = cls.string_to_private_key(data['encoded_private_key'])
        timestamp = datetime.fromisoformat(data['timestamp'])
        return cls(data['name'], data['email'], None, public_key, private_key, timestamp)

    @classmethod
    def remove_pem_headers(cls, pem_key):
        lines = pem_key.strip().splitlines()
        pem_body = ''.join(line for line in lines if not (line.startswith('-----') and line.endswith('-----')))
        return pem_body
