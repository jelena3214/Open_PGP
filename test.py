# from AsymmetricEncription.RSAEncription import RSAEncription
#
# enc = RSAEncription()
#
# pub, _ = enc.generate_rsa_key_set(1024)
#
# print(pub.public_bytes(encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo).hex())
from Cryptodome.Cipher import CAST
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.Random import get_random_bytes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_key_pair():
    # Generisanje RSA ključeva
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Standardna vrednost za javni eksponent
        key_size=2048,  # Dužina ključa (u bitima)
    )
    return private_key


def decrypt_private_key(encrypted_private_key, cast_key):
    # Kreiranje šifrača sa CAST-128 algoritmom
    cipher = CAST.new(cast_key, CAST.MODE_ECB)

    # Dešifrovanje šifrovanog privatnog ključa
    decrypted_private_key_padded = cipher.decrypt(encrypted_private_key)

    # Uklanjanje PKCS7 padding-a
    decrypted_private_key = unpad(decrypted_private_key_padded, 8)

    return decrypted_private_key

def encrypt_private_key(private_key, cast_key):
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()  # Bez šifrovanja privatnog ključa
    )

    # Dodavanje PKCS7 padding-a
    padded_private_key = pad(private_key_pem, 8)

    # Kreiranje šifrača sa CAST-128 algoritmom
    cipher = CAST.new(cast_key, CAST.MODE_ECB)

    # Šifrovanje privatnog ključa
    ciphertext = cipher.encrypt(padded_private_key)

    return ciphertext


# Generisanje RSA ključeva
private_key = generate_rsa_key_pair()

print("RSA KEY: ", private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()  # Bez šifrovanja privatnog ključa
))

# Generisanje ključa za CAST-128 šifrovanje
cast_key = get_random_bytes(16)  # 128-bitni ključ za CAST-128

# Šifrovanje RSA privatnog ključa
encrypted_private_key = encrypt_private_key(private_key, cast_key)

print("Šifrovan RSA privatni ključ:", encrypted_private_key)

decrypted_private_key = decrypt_private_key(encrypted_private_key, cast_key)

print("Dešifrovan RSA privatni ključ:", decrypted_private_key)