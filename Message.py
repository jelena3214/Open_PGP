import ast
import secrets
from datetime import datetime
import zlib
import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from KeyRings.PrivateKey import PrivateKey
from KeyRings.PrivateKeyRing import PrivateKeyRing
from KeyRings.PublicKey import PublicKey
from KeyRings.PublicKeyRing import PublicKeyRing
from SymmetricEncryption.AES128 import AES128
from SymmetricEncryption.TripleDES import TripleDES
from UI.ErrorDialog import show_error_message

"""
Message structure:

Receiver key ID
Encrypted session key
Signature Timestamp
Signer key ID
Leading two octets of signed hash value
Signature
Message Timestamp
Message Content
"""

HEADER_LENGTH = 7


class Message:

    @classmethod
    def send_message(cls, signed, encrypted, compressed, radix64, symmetric_algo, sender_email, receiver_email,
                     message_content, sender_decrypted_private_key, private_key_sender: PrivateKey,
                     receiver_public_key: PublicKey, filepath):
        timestamp = datetime.now()

        # Generate message header
        header = cls.generate_header(signed, encrypted, compressed, radix64, symmetric_algo, sender_email,
                                     receiver_email)

        message = str(timestamp) + '\n' + message_content

        if signed:
            timestamp = datetime.now()
            sender_key_id = private_key_sender.key_id

            data = f"{message_content}{timestamp}".encode('utf-8')

            digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
            digest.update(data)
            hash_value = digest.finalize()
            leading_two_octets = hash_value[0:2]

            signature = sender_decrypted_private_key.sign(
                hash_value,
                padding.PKCS1v15(),
                hashes.SHA1()
            )

            message += '\n' + str(signature) + '\n' + str(leading_two_octets) + '\n' + str(sender_key_id) + '\n' + str(
                timestamp)

        if compressed:
            message = zlib.compress(message.encode('utf-8'))
        else:
            message = message.encode('utf-8')

        if encrypted:
            receiver_key_id = receiver_public_key.key_id

            if symmetric_algo == 'AES128':
                cypher = AES128()
                session_key = secrets.token_bytes(16)
                message = cypher.encrypt_cfb64(message, session_key)
            else:
                cypher = TripleDES()
                session_key = secrets.token_bytes(24)
                message = cypher.encrypt_cfb64(message, session_key)

            encrypted_ks = receiver_public_key.public_key.encrypt(
                session_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            message = str(receiver_key_id) + '\n' + str(encrypted_ks) + '\n' + str(message)
        else:
            message = str(message)

        if radix64:
            message = cls.encode_radix64(message)

        message = header + '\n' + message

        with open(filepath, "w") as file:
            file.write(message)

        return message

    @classmethod
    def generate_header(cls, signed, encrypted, compressed, radix64, symmetric_algo, sender_email, receiver_email):
        return (f"From:{sender_email}\n"
                f"To:{receiver_email}\n"
                f"Signed:{signed}\n"
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

        return (header_dict.get("From"),
                header_dict.get("To"),
                header_dict.get("Signed") == "True",
                header_dict.get("Encrypted") == "True",
                header_dict.get("Compressed") == "True",
                header_dict.get("Radix64") == "True",
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

    @classmethod
    def parse_received_data(cls, filepath, private_key_ring: PrivateKeyRing):
        with open(filepath, 'r') as file:
            message = file.read()
        try:
            header_lines = message.splitlines()
            header = "\n".join(header_lines[:HEADER_LENGTH])
            sender, receiver, signed, encrypted, compressed, radix64, algo = cls.parse_header(header)

            message = "\n".join(header_lines[HEADER_LENGTH:])

            if radix64:
                message = cls.decode_radix64(message)

            receiver_private_key = None
            encrypted_ks_str = None
            if encrypted:
                receiver_key_id_str, encrypted_ks_str, message = message.rsplit('\n', 2)
                receiver_private_key = private_key_ring.get_key_by_key_id(receiver_key_id_str)

            return receiver_private_key, message, encrypted_ks_str, algo, compressed, signed, encrypted, sender, receiver
        except BaseException:
            raise

    @classmethod
    def receive_message(cls, message, passphrase, receiver_key: PrivateKey, encrypted_ks_str,
                        public_key_ring: PublicKeyRing, algo, compressed, signed, encrypted):
        try:
            # From str to bytes
            message = bytes(ast.literal_eval(message))

            if encrypted:
                receiver_private_key = receiver_key.decrypt_private_key(passphrase)

                # Message content will be None
                if receiver_private_key is None:
                    show_error_message("Pogrešna lozinka za dati privatni ključ!")
                    return

                encrypted_session_key = bytes(ast.literal_eval(encrypted_ks_str))
                session_key = receiver_private_key.decrypt(
                    encrypted_session_key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )

                if algo == 'AES128':
                    cypher = AES128()
                    message = cypher.decrypt_cfb64(message, session_key)
                else:
                    cypher = TripleDES()
                    message = cypher.decrypt_cfb64(message, session_key)

            if compressed:
                message = zlib.decompress(message).decode('utf-8')
            else:
                message = message.decode('utf-8')

            if signed:
                parts = message.split('\n')

                message_timestamp = parts[0]
                message_content = "\n".join(parts[1:-4])

                signature_str = parts[-4]
                signature = bytes(ast.literal_eval(signature_str))
                leading_two_octets_str = parts[-3]
                leading_two_octets = bytes(ast.literal_eval(leading_two_octets_str))
                sender_key_id = parts[-2]
                signature_timestamp = parts[-1]

                sender_key_pair = public_key_ring.get_key_by_key_id(sender_key_id)

                if sender_key_pair is None:
                    show_error_message(
                        "Ne postoji potreban ključ iz prstena javnih ključeva za proveru potpisa poruke!")
                    return

                data = f"{message_content}{signature_timestamp}".encode('utf-8')

                digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
                digest.update(data)
                hash_value = digest.finalize()
                leading_two_octets_received = hash_value[0:2]

                try:
                    if leading_two_octets_received != leading_two_octets:
                        print('Vrednost okteta se ne poklapa!')
                        raise InvalidSignature

                    sender_key_pair.public_key.verify(
                        signature,
                        hash_value,
                        padding.PKCS1v15(),
                        hashes.SHA1()
                    )
                except InvalidSignature:
                    print("Signature verification failed.")
                    raise
            else:
                parts = message.split('\n')

                message_timestamp = parts[0]
                message_content = "\n".join(parts[1:])

            return (f"Timestamp:{message_timestamp}\n"
                    f"Content:{message_content}")
        except InvalidSignature:
            raise InvalidSignature
        except BaseException as e:
            raise
