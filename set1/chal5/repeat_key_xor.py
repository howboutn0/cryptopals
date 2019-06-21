import binascii
string = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = 'ICE'
#both are ascii
def repeat_key_xor(string, key):
	#ascii_string = binascii.unhexlify(string)
	res = ""
	temp_key = 0
	#counter
	#ex: if the counter is at 3 and the word is ICE, that means 0 was I, 1 was C, 2 was E and now 3 is I
	letter = 0
	for char in string:
		temp_key = key[letter % len(key)]
		res = res + chr(ord(char) ^ ord(temp_key))
		letter += 1
	print res.encode('hex')
	return res

repeat_key_xor(string, key)