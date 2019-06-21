from Crypto.Cipher import AES

import base64

"""
1. take a line as input
2. split it into groups of 16
3. find duplicate groups
	create a hashset
	try looking the next block in the hashset
		if it shows up, then that's the correct answer
		otherwise, just add it in
"""
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

with open('file') as input_file:
	for line in input_file.readlines():
		ciphertext = base64.b64decode(line.rstrip())
		if detect(ciphertext):
			print ciphertext
			print base64.b64encode(ciphertext)
			print "YA YEET"