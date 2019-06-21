#!/bin/env/python3
from Crypto.Cipher import AES
import random
def parse(byte_string):
    string = byte_string.decode()
    result = dict(pair.split('=') for pair in string.split('&'))
    return result
def profile_for(email):
    if b"&" in email or b"=" in email:
        raise ValueError("Invalid email address")
    return b"email=" + email + b'&uid=10&role=user'

def gen_x_bytes(x):
    b = b''
    for i in range(x):
        r = random.randint(0, 127)
        b += bytes(chr(r), 'ascii')
    return b
def gen_random_key():
    return gen_x_bytes(16)

key = gen_random_key()

def encrypt_profile_for(email):
    cipher = AES.new(key, AES.MODE_ECB)
    encoded_profile = pad(profile_for(email), 16)
    return cipher.encrypt(encoded_profile)

def unpadPKCS7(s, k):
    i = s[-1]
    return s[0:-i]

def pad(string, blocklength):
    n = (blocklength - (len(string) % blocklength)) % blocklength
    return string + str.encode(n*chr(n))

def decrypt_profile(s):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_profile = unpadPKCS7(cipher.decrypt(s), 16)
    pairs = decrypted_profile.split(b'&')
    profile = []
    for p in pairs:
        profile += [[x.decode('ascii') for x in p.split(b'=')]]
    return profile

#print(parse(b'foo=bar&baz=qux&zap=zazzle'))

#print(profile_for(b"foo@bar.com"))

#print(encrypt_profile_for(b"e"*32 + b"@mail.com"))
#print(decrypt_profile(encrypt_profile_for(b"e"*32 + b"@m.com")))

#23 bytes
#11 bytes

def get_blocks(plaintext):
    return [plaintext[i: i+16] for i in range(0, len(plaintext), 16)]

def get_encrypted_blocks(ciphertext):
    return [ciphertext[i: i + 16] for i in range(0, len(ciphertext), 16)]
#length 13 + 16x is good for payload
prefix = b'a' * 16
payload = prefix + b'yay@gmail.com'

#print(pad(b'admin', 16))
#payload2 = payload + pad(b'admin', 16)

#print("profile: " + str(profile_for(payload2)))
#print("plaintext blocks: " + str(get_blocks(profile_for(payload2))))
#print("encrypted: " + str(encrypt_profile_for(payload2)))
#print("ciphertext blocks: " + str(get_encrypted_blocks(encrypt_profile_for(payload2))))
#print("decrypted: " + str(decrypt_profile(encrypt_profile_for(payload2))))

#print(pad(b'admin', 16))
#payload2 = payload + pad(b'admin', 16)

#step 1: extract the ciphertext when role is the last block
#get rid of the last block, keep the rest of the ciphertext
encrypted_profile = encrypt_profile_for(payload)
encrypted_blocks = get_blocks(encrypted_profile)

res = b''
for i in range(len(encrypted_blocks) - 1):
    res += encrypted_blocks[i]
print(encrypted_profile)
print(encrypted_blocks)
print('\n')
print(res)

padded_adm = pad(b'admin', 16)
payload2 = 10*b'a' + padded_adm + payload

profile2 = profile_for(payload2)
plaintext_blocks = get_blocks(profile2)
print(plaintext_blocks)
encrypted_profile2 = encrypt_profile_for(payload2)
encrypted_blocks2 = get_blocks(encrypted_profile2)

adm = encrypted_blocks2[1]

final = res + adm
print(decrypt_profile(final))
