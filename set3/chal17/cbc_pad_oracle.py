from Crypto.Cipher import AES
import random
def is_pkcs7_padded(binary_data):
    """Returns whether the data is PKCS 7 padded."""

    # Take what we expect to be the padding
    padding = binary_data[-binary_data[-1]:]

    # Check that all the bytes in the range indicated by the padding are equal to the padding value itself
    return all(padding[b] == len(padding) for b in range(0, len(padding)))


def validate(data):
    """Unpads the given data from its PKCS 7 padding and returns it."""
    if len(data) == 0:
        raise Exception("The input data must contain at least one byte")

    if not is_pkcs7_padded(data):
        return data

    padding_len = data[len(data) - 1]
    return data[:-padding_len]
def pad(string, blocklength):
    n = (blocklength - (len(string) % blocklength)) % blocklength
    return string + str.encode(n*chr(n))

def gen_x_bytes(x):
    b = b''
    for i in range(x):
        r = random.randint(0, 127)
        b += bytes(chr(r), 'ascii')
    return b
def gen_random_key():
    return gen_x_bytes(16)

key = gen_random_key()
IV = gen_random_key()

strings = [
    b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
    b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
    b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
    b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
    b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
    b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
    b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
    b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
    b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
    b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
]

def pick_string():
    return strings[random.randint(0, len(strings))]

def encrypt():
    string = pick_string
    padded_str = pad(string, 16)
    cipher = AES.new(key, AES.MODE_CBC, IV)
    return cipher.encrypt(padded_str)

def decrypt(ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, IV)
    plaintext = cipher.decrypt(ciphertext)
    return is_pkcs7_padded(plaintext)

def get_blocks(string):
    return [string[i: i+16] for i in range(0, len(string), 16)]
def guess():
    ct = encrypt()
    #get last byte

def gen_c1():
    b = b''
    for i in range(16):
        r = random.randint(17, 255)
        b += bytes([r])
    return b

def change_char(s, p, r):
    return s[:p]+r+s[p+1:]

def xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

#byte can be 15 --> 0
#ex: guessing byte 15 means xor w 16 - 15
def xor_byte_x(c1_prime, byte):
    val = 16 - byte
    #ex: changing the 2nd to last byte
    #c1_prime[14] xor b'\x02'
    return xor(c1_prime[byte], bytes([val]))
#guess bytes from 15 --> 0
def get_last_byte(ct, block, IV, byte):
    #setup c1 and c2
    blocks = get_blocks(ct)
    c2 = ct[block]
    c1 = gen_c1()
    #setup a fake dk_c2 and p2 that gradually change
    dk_c2 = b'a'*16
    p2 = b'b'*16
    #aight time to guess and check
    for i in range(0, 256):
        #create c1
        guess = bytes([i])
        c1_prime = change_char(c1, byte, guess)
        #we did it bois
        if(decrypt(c1_prime + c2)):
            dk_c2 = change_char(dk_c2, xor_byte_x())
