from cryptography.hazmat.primitives import serialization

class KeyOperator:
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