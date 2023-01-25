from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

import base64
import zlib


PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuNqO7IhSaA164VYRaQeq
EaKdKpBgy7ZuI7zKsGLZgehZ5/H5GZCy0fhKcdZsbbwe2stLVYCQzgTKNBA16y/a
G1xMViSbAWHZXLxyEn2GIcbmd6tEmuwuielGLtNuIx18q6WSLx8x9H4gO5EYVRkL
Gnx9xBiPkpbjUIc4qzZy9yfUO/zZ3vk4uIuXVDlWIfgf31GN+jP2R+Dx3CJxWefx
ZzAcQrmLv3BVZ0Kw0Il14Zn2YjnDI0oJr5dJV6tA6TUqMzH7Q6llwkaP3lLBSwTF
Q8EZwOaEKn7xKax/ypnYJJChr9oYDysDR0HLfaWYx9gz3AdUwSSvjKVTCmju3/pP
MQIDAQAB
-----END PUBLIC KEY-----"""

def encrypt(plain_text_bytes):
    compressed_text = zlib.compress(plain_text_bytes)
    session_key = get_random_bytes(16)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(compressed_text)

    rsa_key = RSA.importKey(PUBLIC_KEY)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_session_key = cipher_rsa.encrypt(session_key)

    payload = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    encrypted = base64.encodebytes(payload)
    return(encrypted)

def encrypt_file(file_name):
    with open(file_name, "rb") as file:
        plain_text_bytes = file.read()

    encrypted_data = encrypt(plain_text_bytes)

    with open(file_name, "wb") as file:
        file.write(encrypted_data)

if __name__ == "__main__":
    encrypt_file("hh.txt")
