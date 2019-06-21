#!/usr/bin/python3
import random
import sys
from Crypto.Cipher import AES
import base64
from Crypto.Util.strxor import strxor

def gen_x_bytes(x):
    b = b''
    for i in range(x):
        r = random.randint(0, 127)
        b += bytes(chr(r), 'ascii')
    return b
def gen_random_key():
    return gen_x_bytes(16)

def cbc_encrypt(plaintext,key, IV):
    #split the plaintext into blocks of size 16 bytes
    blocks = [plaintext[i: i + 16] for i in range(0, len(plaintext), 16)]
    c = AES.new(key, AES.MODE_ECB)
    #IV = b"\x00"*16
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

def pad(string, blocklength):
    n = (blocklength - (len(string) % blocklength)) % blocklength
    #print(string + n*chr(n))
    #print(repr(string + n*chr(n)))
    return string + str.encode(n*chr(n))

def encryption_oracle(plaintext):
    r1 = random.randint(5, 10)
    r2 = random.randint(5, 10)
    padded = gen_x_bytes(r1) + str.encode(plaintext) + gen_x_bytes(r2)
    padded = pad(padded, 16)
    mode = random.randint(1,2)

    if mode == 1:
        c = AES.new(gen_random_key(), AES.MODE_ECB)
        print("mode 1")
        return c.encrypt(padded)
    else:
        print("mode 2")
        return cbc_encrypt(padded, gen_random_key(), gen_random_key())

def detect(line):
    if len(line) %16 != 0:
        return False
    blocks = [line[i: i + 16] for i in range(0, len(line), 16)]
    s = set()
    for block in blocks:
        if block in s:
            return True
        s.add(block)
    return False

def guess(plaintext):
    if detect(plaintext):
        print("ECB")
    else:
        print("CBC")

offset = gen_x_bytes(random.randint(1, 15))
print('real offset len: ' + str(len(offset)))
def ecb_encrypt(s):
    key = 'YELLOW SUBMARINE'
    x = base64.b64decode(open('file').read())
    cipher = AES.new(key, AES.MODE_ECB)
    s = pad(offset + s + x, 16)
    return cipher.encrypt(s)

def getoffset():
    for i in range(1, 16):
        inject = i * b'a' + b'abcdefghijklmnop'*2
        string = ecb_encrypt(inject)
        if detect(string):
            return i
    return 17
"""awk '$1=="ec:"{ec=$2}$1=="s3:"{s3=$2}END{print "ec:"ec, "s3:"s3}' $file

How to do the attack:
ex:
pt: AAAAAAAA secret123
ct: 02kcf123 2kdma1k24

once u shift the A's down, u fill in the slot with 1 of the plaintext secret characters

ex:
note: X can be just wtvr
pt: AAAAAAAs ecret123X
ct: dk02cl2f 292f1dk32

but u didn't know that it was s because u don't have the pt irl
so can start guessing combinations of AAAAAAA[?]
ex: guess AAAAAAAa --> AAAAAAAZ
until one of them matches dk02cl2f after encryption

then u have 1 byte of the plaintext

once u figure out that it is 's' (in this example at least)
shift it down again

ex:

pt: AAAAAAse cret123XX
ct: gk1lr0el kp2284fbs

now, the controlled prefix becomes AAAAAAs
and then we can guess all AAAAAAs[?]
"""


def brute_force():
    prefix_length = 144
    known = 0
    unknown = 139
    known_bytes = b''
    offset = getoffset()
    print(offset)
    while(known < unknown):
        p = offset*b'z' + (prefix_length - known - 1)*b'A'
        res = ecb_encrypt(p)[0:prefix_length+offset]
        for i in range(128):
            p2 = p + known_bytes + bytes(chr(i), 'ascii')
            guess = ecb_encrypt(p2)[0:prefix_length+offset]
            if guess == res:
                known += 1
                known_bytes += bytes(chr(i), 'ascii')
                print(known_bytes)
                break
brute_force()
