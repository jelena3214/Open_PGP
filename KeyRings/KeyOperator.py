from datetime import datetime

from cryptography.hazmat.primitives import serialization

import context
from KeyRings.PrivateKey import PrivateKey


class KeyOperator:
    @classmethod
    def export_key_metadata(cls, timestamp, email, name, file_path):
        timestamp_str = timestamp.isoformat()

        with open(file_path, 'wb') as pem_file:
            pem_file.write(timestamp_str.encode('utf-8'))
            pem_file.write(b'\n')
            pem_file.write(email.encode('utf-8'))
            pem_file.write(b'\n')
            pem_file.write(name.encode('utf-8'))
            pem_file.write(b'\n')

    @classmethod
    def export_public_key_to_pem(cls, timestamp, email, name, public_key, file_path):
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        cls.export_key_metadata(timestamp, email, name, file_path)

        with open(file_path, 'ab') as pem_file:
            pem_file.write(pem_data)

    @classmethod
    def export_key_set_to_pem(cls, private_key_struct, file_path):
        private_key = private_key_struct.private_key_as_string()
        timestamp = private_key_struct.timestamp
        email = private_key_struct.email
        name = private_key_struct.name

        public_key = private_key_struct.public_key
        cls.export_public_key_to_pem(timestamp, email, name, public_key, file_path)

        with open(file_path, 'ab') as pem_file:
            pem_file.write(private_key.encode('utf-8'))

    @classmethod
    def import_public_key_from_pem(cls, file_path):
        with open(file_path, 'rb') as pem_file:
            content = pem_file.read().decode('utf-8')

        metadata_end_index = content.index('-----BEGIN PUBLIC KEY-----')
        metadata = content[:metadata_end_index].strip().split('\n')

        timestamp = datetime.fromisoformat(metadata[0])
        email = metadata[1]
        name = metadata[2]

        public_key_start = content.index('-----BEGIN PUBLIC KEY-----')
        public_key_end = content.index('-----END PUBLIC KEY-----') + len('-----END PUBLIC KEY-----')
        public_key_data = content[public_key_start:public_key_end].encode('utf-8')

        public_key = serialization.load_pem_public_key(public_key_data)
        if not context.public_key_ring.add_new_public_key(name, email, public_key, timestamp):
            return None, None, None, None

        return name, email, public_key, timestamp

    @classmethod
    def import_key_set_from_pem(cls, file_path):
        with open(file_path, 'rb') as pem_file:
            content = pem_file.read().decode('utf-8')

        private_key_start = content.index('-----END PUBLIC KEY-----') + len('-----END PUBLIC KEY-----\n')
        private_key_data = content[private_key_start:]
        assert (len(private_key_data) > 0)

        name, email, public_key, timestamp = cls.import_public_key_from_pem(file_path)
        if name is None:
            return False

        private_key = PrivateKey.string_to_private_key(private_key_data)
        context.private_key_ring.add_new_private_key(name, email, public_key, private_key, None, timestamp)
        return True
