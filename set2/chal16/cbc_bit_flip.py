from Crypto.Cipher import AES
from bitstring import BitArray
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

"""
prepare the input string
prepend and append some information
"""
def prepare(string):
    string = string.replace(b';', b'').replace(b'=', b'')
    return b"comment1=cooking%20MCs;userdata=" + string + b";comment2=%20like%20a%20pound%20of%20bacon"

key = b"YELLOW SUBMARINE"
IV = b"YELLOW SUBMARINE"

def encrypt(string):
    string = pad(prepare(string), 16)
    c = AES.new(key, AES.MODE_CBC, IV)
    res = c.encrypt(string)
    print(res)
    return res

def decrypt(ciphertext):
    c = AES.new(key, AES.MODE_CBC, IV)
    pt = c.decrypt(ciphertext)
    v = validate(pt)
    if b";admin=true;" in v:
        print("gottem")
    else:
        print("nope")
    return v

def get_blocks(string):
    return [string[i: i + 16] for i in range(0, len(string), 16)]

#t = encrypt(b"yayeee")
#print(t)
#print(get_blocks(t))
#d = decrypt(t)
#print(d)

#b = get_blocks(d)
#print(b)

ciphertext = encrypt(b'yayeee')
cblocks = get_blocks(ciphertext)
plaintext = decrypt(ciphertext)
pblocks = get_blocks(plaintext)

desired = b';admin=true;\x00\x00\x00\x00'
print(len(desired))

def xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

c1 = xor(xor(pblocks[2], cblocks[1]), desired)

new_ct = cblocks[0] + c1 + cblocks[2] + cblocks[3] + cblocks[4]

print(decrypt(new_ct))
