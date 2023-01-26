import base64
import pathlib

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAuNqO7IhSaA164VYRaQeqEaKdKpBgy7ZuI7zKsGLZgehZ5/H5
GZCy0fhKcdZsbbwe2stLVYCQzgTKNBA16y/aG1xMViSbAWHZXLxyEn2GIcbmd6tE
muwuielGLtNuIx18q6WSLx8x9H4gO5EYVRkLGnx9xBiPkpbjUIc4qzZy9yfUO/zZ
3vk4uIuXVDlWIfgf31GN+jP2R+Dx3CJxWefxZzAcQrmLv3BVZ0Kw0Il14Zn2YjnD
I0oJr5dJV6tA6TUqMzH7Q6llwkaP3lLBSwTFQ8EZwOaEKn7xKax/ypnYJJChr9oY
DysDR0HLfaWYx9gz3AdUwSSvjKVTCmju3/pPMQIDAQABAoIBAAcXagc8nZNcp7D6
/nT93xzealLGh31uf2At7xqq2CGfL8pxonbuxvq+IIuocwVsrkRXgImEV/RyA5h8
DLgmivf6ElBLBt/xMzJXD7XnjIdBhvg39kxOhjndMfI8QzaOpt3mNABMcpFTa1oi
/ADREqIj/NEn3g4nbWCv/KZjfYU/YwrkGQ4stiBnHdAJhhVqOGUEq/xcXv3qHGD1
rtPXIsH76RvROkoH4K5JZW01Q5NjNeZd7EXBcMQcU3BjyuAik74/fE3/IXa2z6jJ
FHL4WQk359S/I8e5wNHY/OEQOBxPdpoglNLUvlRlqMsYQALmbcD/L6i85Vjk61X/
vkQD3ucCgYEA0XpHlmp5XkXJa1O/tm6nD9KvvEsIDywQHYlTUWMlq/Eg/LM2SDtN
ZywV/owzbeXq0c3W0BnUPrkfansxS8JZwTejTT9dDzIpWSF3bgrbFeXr4HP7J1Lx
ro4TjZDLOqih3cOPGu0oklJipw/RXu86jeEzVe/o1r4jh72zL6xonOMCgYEA4ehN
OQqX4wYSVedBsZf2lBKQpP9jfwQ3XoYn0UCZ7CZzRhPQgKsid8KkayIJR1XndKfR
neUNvpYIUYJJ3sIS94kiyvy8Zfzq/nh9/1xAskdaWjUuPZzuqo8PElzbroT8xl/g
lrmMnZvLa496IsBAlVs1rb1wyUQej6ga4Y6v09sCgYEAuUMlFwGZz2d3COXrssPQ
Gq1h4OyW9xwoMIcoWd2PDq9WVkeFJYLVJP8XgKWsQnDKKb2bUzbUwJhnEXxcj70W
Nk0nrwTwH6VkbkCr6HXPZ2GOKFdK829m8dMTtest4fYMGh5/bPf8HtSgDVJvAEAh
kCNwjHt+eJV2xPFgDTS03LMCgYEA0gUlxeITUvxSD4rviCu/EeowjzTfSzagQ0B1
xBRLBUC56myBax2u7agHM5JxDeDPTaS3PBO2s3jIQv7drjq/Z2IW9qAAhtCbp/hd
KwqZGyU62qKWWrGLMQXO/UNW+OiqF8MLCRV3pQ8yDs1Uvvn9EN27CcsVEAhEYUnn
s8rzrAECgYACyIKywNLQhTFhiKNlhMPsN+r62Hji/TBhQZ6djsslCv/AVHaEli0n
u3JcI5yBT+iGZkL+3jTF9E9wKdHMRavxzD+Ke3GPBZgMduU1cnYx66pFOjqNaxJc
ta5iHp+3Kmj4VJqEsScOUnRkE4ngwreVa06VH3jweVcHFtuJZVuiTA==
-----END RSA PRIVATE KEY-----"""

def decrypt_ransom_key(encrypted):
    encrypted_bytes = base64.b64decode(encrypted.encode("ASCII"))
    rsa_private_key = RSA.importKey(PRIVATE_KEY)
    rsa_cipher = PKCS1_OAEP.new(rsa_private_key)
    ransom_key = rsa_cipher.decrypt(encrypted_bytes)
    return ransom_key

def get_ransom_key(mac):
    file_name = ""
    for child in pathlib.Path("data").glob("*"):
        if child.is_file():
            file_name = str(child)
            if mac in file_name and "ransomware" in file_name:
                break

    if file_name == "":
        return -1
    with open(file_name, "r") as f:
        encrypted_ransom_key = f.read()
    ransom_key = decrypt_ransom_key(encrypted_ransom_key)
    return base64.encodebytes(ransom_key)

if __name__ == "__main__":
    r_key = get_ransom_key("O13")
    print(r_key)
