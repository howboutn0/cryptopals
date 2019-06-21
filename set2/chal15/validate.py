#!/usr/bin/python3

def validate(string):
    pad_len = ord(string[len(string) - 1:])
    orig = string[0:len(string) - pad_len]
    expected = pad(orig, len(string))
    if expected == string:
        return orig
    raise Exception("ha you're fucking dumb")
def pad(string, blocklength):
    n = (blocklength - (len(string) % blocklength)) % blocklength
    return string + str.encode(n*chr(n))

print(validate(b"ICE ICE BABY\x04\x04\x04\x04"))
