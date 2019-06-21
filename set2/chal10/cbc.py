"""import base64
from Crypto.Cipher import AES

x = base64.b64decode(open('7.txt', 'r').read())

key = b'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB)
y = cipher.decrypt(x)
print(y)
"""
from Crypto.Cipher import AES
import base64
from Crypto.Util.strxor import strxor

def cbc_encrypt(plaintext,key):
    #split the plaintext into blocks of size 16 bytes
    blocks = [plaintext[i: i + 16] for i in range(0, len(plaintext), 16)]
    c = AES.new(key, AES.MODE_ECB)
    IV = b"\x00"*16
    ciphertext = b""
    prev = IV
    for plaintext_block in blocks:
        cipherblock = c.encrypt(strxor(plaintext_block, prev))
        ciphertext += cipherblock
        prev = cipherblock
    return ciphertext
def cbc_decrypt(ciphertext, key):
    blocks = [ciphertext[i: i + 16] for i in range(0, len(ciphertext), 16)]
    plaintext = b""
    c = AES.new(key, AES.MODE_ECB)
    prev = b"\x00"*16
    for cipherblock in blocks:
        plaintext_block = strxor(c.decrypt(cipherblock), prev)
        plaintext += plaintext_block
        prev = cipherblock
    return plaintext


x = base64.b64decode(open('file').read())
decrypted = cbc_decrypt(x, b'YELLOW SUBMARINE')
print(decrypted)
print(base64.b64encode(cbc_encrypt(decrypted, b'YELLOW SUBMARINE')))
