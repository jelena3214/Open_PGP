from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from Exceptions.PGPException import PGPException


class RSAEncryption:

    @classmethod
    def generate_rsa_key_set(cls, key_size):
        if key_size != 1024 and key_size != 2048:
            raise PGPException("Key size for RSA is not valid!")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        return public_key, private_key
