import binascii
string = 0x1c0111001f010100061a024b53535009181c
key = 0x686974207468652062756c6c277320657965

bin_string = bin(string)
bin_key = bin(key)

xor = int(bin_string, 2) ^ int(bin_key, 2)
print hex(xor)
