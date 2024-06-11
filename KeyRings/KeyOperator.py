from cryptography.hazmat.primitives import serialization


class KeyOperator:
    @classmethod
    def export_public_key_to_pem(cls, public_key, file_path):
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(file_path, 'wb') as pem_file:
            pem_file.write(pem_data)

    @classmethod
    def export_key_set_to_pem(cls, private_key_struct, passphrase, file_path):
        private_key = private_key_struct.decrypt_private_key(passphrase)
        if private_key is None:
            return False

        public_key = private_key_struct.public_key
        cls.export_public_key_to_pem(public_key, file_path)

        pem_data_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(file_path, 'ab') as pem_file:
            pem_file.write(pem_data_private)

        return True

    @classmethod
    def import_public_key_from_pem(cls, file_path):
        with open(file_path, 'rb') as pem_file:
            pem_data = pem_file.read()

        public_key = serialization.load_pem_public_key(pem_data)

        return public_key

    #TODO: Should it be encrypted?
    @classmethod
    def import_private_key_from_pem(self, file_path):
        with open(file_path, 'rb') as pem_file:
            pem_data = pem_file.read()

        private_key = serialization.load_pem_private_key(
            pem_data,
            password=None,
        )

        return private_key

    @classmethod
    def remove_pem_headers(cls, pem_key):
        lines = pem_key.strip().splitlines()
        pem_body = ''.join(line for line in lines if not (line.startswith('-----') and line.endswith('-----')))
        return pem_body

