import secrets
from datetime import datetime
import zlib
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from SymmetricEncryption.AES128 import AES128
from SymmetricEncryption.TripleDES import TripleDES


class Message:

    # signature, encrypted, symmetric_algo, compressed, radix64
    @classmethod
    def send_message(cls, signed, encrypted, compressed, radix64, symmetric_algo, message_content, sender_private_key,
                     sender_key_id, receiver_public_key, receiver_key_id, filepath):
        timestamp = datetime.now()
        # Generate message header
        header = cls.generate_header(signed, encrypted, compressed, radix64, symmetric_algo)

        message = str(timestamp) + '\n' + message_content

        # Signature
        if signed:
            data = f"{message}{timestamp}".encode('utf-8')

            digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
            digest.update(data)
            hash_value = digest.finalize()
            leading_two_octates = hash_value[0:2]

            signature = sender_private_key.sign(
                hash_value,
                padding.PKCS1v15(),
                hashes.SHA1()
            )

            message += str(timestamp) + '\n' + str(sender_key_id) + '\n' + str(leading_two_octates) + '\n' + str(
                signature) + '\n'

        if compressed:
            message = zlib.compress(message.encode('utf-8'))

        if encrypted:
            if symmetric_algo == 'AES128':
                cypher = AES128()
                session_key = secrets.token_bytes(16)
                message = cypher.encrypt_cfb64(message, session_key)
            else:
                cypher = TripleDES()
                session_key = secrets.token_bytes(24)
                message = cypher.encrypt_cfb64(message, session_key)

            #kriptovan sesisijski kljuc i key id recip
            encrypted_ks = receiver_public_key.public_key.encrypt(
                session_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            message += str(encrypted_ks) + '\n' + str(receiver_key_id)

        if radix64:
            message = cls.encode_radix64(message)

        message = header + '\n' + message

        with open(filepath, "w") as file:
            file.write(message)

        return message


    @classmethod
    def receive_message(cls):
        pass

    @classmethod
    def generate_header(cls, signed, encrypted, compressed, radix64, symmetric_algo):
        return (f"Signed:{signed}\n"
                f"Encrypted:{encrypted}\n"
                f"Compressed:{compressed}\n"
                f"Radix64:{radix64}\n"
                f"Algo:{symmetric_algo}")

    @classmethod
    def parse_header(cls, header):
        lines = header.split("\n")
        header_dict = {}

        for line in lines:
            key, value = line.split(":")
            header_dict[key] = value

        return (header_dict.get("Signed"),
                header_dict.get("Encrypted"),
                header_dict.get("Compressed"),
                header_dict.get("Radix64"),
                header_dict.get("Algo"))

    @classmethod
    def encode_radix64(cls, data):
        data_bytes = data.encode('utf-8')
        encoded_data = base64.b64encode(data_bytes)
        encoded_string = encoded_data.decode('utf-8')

        return encoded_string

    @classmethod
    def decode_radix64(cls, encoded_string):
        encoded_bytes = encoded_string.encode('utf-8')
        decoded_data = base64.b64decode(encoded_bytes)
        decoded_string = decoded_data.decode('utf-8')

        return decoded_string