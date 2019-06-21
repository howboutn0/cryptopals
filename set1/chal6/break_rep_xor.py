import base64
import math
import binascii
#input: ascii text
#output: the binary representation, but in string form
#s1 and s2 are ascii text input
def hamming(s1, s2):
	s1_bytes = bytearray(s1)
	s2_bytes = bytearray(s2)
	diff = 0
	for i in range(0, len(s1_bytes)):
		x = pad(str(bin(s1_bytes[i]))[2:])
		y = pad(str(bin(s2_bytes[i]))[2:])
		diff += difference(x, y)
	#print diff
	return diff

#take in a string of 1s and 0s. make it length 8
def pad(s):
	return (8-len(s))*'0' + s

#bin1 and bin2 are strings
def difference(bin1, bin2):
	count = 0
	for i in range(0, len(bin1)):
		if(bin1[i] != bin2[i]):
			count += 1
	return count
x = 'this is a test'
y = 'wokka wokka!!!'
hamming(x, y)

#smaller hamming distance is better
#put that at the front of the list
def compare(x, y):
	if y < x:
		return 1
	elif x < y:
		return -1
	else:
		return 0

#dict maps normalized value to keysize
def find_keysize(string, dict):
	norm = []
	#try different keysizes
	for keysize in range(1, 41):
		try:
			s1 = string[0: keysize]
			s2 = string[keysize: 2*keysize]
			s3 = string[2*keysize : 3*keysize]
			s4 = string[3*keysize : 4*keysize]

			normalized_dist = float(hamming(s1, s2) + hamming(s2, s3) + hamming(s3, s4))/(keysize * 3)
			norm.append(normalized_dist)
			dict[normalized_dist] = keysize
		except:
			pass
	sorted_norm = sorted(norm, cmp=compare)
	#print sorted_norm
	return sorted_norm
dict = {}
#guesses = find_keysize('this is just a test', dict)
#g1 = dict[guesses[0]]
#g2 = dict[guesses[1]]
#g3 = dict[guesses[2]]

#print g1
#print g2
#print g3

def b64_to_ascii(file):
	with open(file) as input_file:
		ciphertext = base64.b64decode(input_file.read())
	return ciphertext

dict = {}
ciphertext = 'KZ6UaztNnau6z39oMHUu8UTvdmq1bhob3CcEFdWXRfxJqdUAiNep4pkvkAZUSn9CvEvPNT5r2zt6JPg9bVBPYuTW4xr8v2PuPxVuCT6MLJWDJp84'
#ciphertext = b64_to_ascii('file')
guesses = find_keysize(ciphertext, dict)

g1 = dict[guesses[0]]
g2 = dict[guesses[1]]
g3 = dict[guesses[2]]

#break the ciphertext into blocks of keysize length
#ex: try breaking it into groups of 2
def split(string, n):
	res = [string[i: i + n]for i in range(0, len(string), n)]
	#print res
	return res

def transpose(string, n):
	x = split(string, n)
	res = []
	#take the ith letter of each jth block in x
	temp = ""
	for i in range(0, n):
		for j in range(0, len(x)):
			try:
				temp += (x[j][i])
			except:
				pass
		if temp != "":
			res.append(temp)
		temp = ""
	return res
	#0th index: 1st letter of each block
	#1st index: 2nd letter of each block
	#2nd index: 3rd letter of each block

#test = transpose('abcdefghijklmnop', 3)
#print test 

def single_hex_xor(string, key):
	#ascii_string = binascii.unhexlify(string)
	ascii_string = string
	res = ""
	for char in ascii_string:
		res = res + chr(ord(char) ^ key)
	return res
#etaoin shrdlu
freq = {'e': .12702, 't': .09056, 'a': .08167, 'o': .07507, 'i': .06966, 'n': .06749, 's': .06327, 'h': .06094, 'r': .05987, 'd': .04253, 'l': .04025, 'u': .02758}

#analyze freq of letter in string
#return a decimal that represents the frequency
def a(string, letter):
	lower = string.lower()
	count = 0.0
	for char in string:
		if char == letter:
			count += 1.0
	return count/len(string)

#return a dictionary of the freq
#etaoin shrdlu
def dictfreq(s):
	res = {'e': a(s, 'e'), 't': a(s, 't'), 'a': a(s, 't'), 'o': a(s, 'o'), 'i': a(s, 'i'), 'n': a(s, 'n'), 's': a(s, 's'), 'h': a(s, 'h'), 'r': a(s, 'r'), 'd': a(s, 'd'), 'l': a(s, 'l'), 'u': a(s, 'u')}
	return res

#dot product of dictionary x and y
def dot(x, y):
	return x['e']*y['e'] + x['t']*y['t'] + x['a']*y['a'] + x['o']*y['o'] + x['i']*y['i'] + x['n']*y['n'] + x['s']*y['s'] + x['h']*y['h'] + x['r']*y['r'] + x['d']*y['d'] + x['l']*y['l'] + x['u']*y['u']

#magnitude
def magn(x):
	res = 0.0
	for key in x:
		res += x[key] ** 2
	return math.sqrt(res)


def cos(x, y):
	if magn(x) == 0 or magn(y) == 0:
		return 0
	return dot(x, y)/(magn(x) * magn(y))

def cos_compare(string1, string2):
	dict1 = dictfreq(string1)
	dict2 = dictfreq(string2)
	cos1 = cos(dict1, freq)
	cos2 = cos(dict2, freq)

	if cos1 > cos2:
		return 1
	elif cos2 > cos1:
		return -1
	else:
		return 0


def bruteforce(string, n):
	print 'hllo'
	trans = transpose(string, n)
	keys = []
	"""for block in trans:
		#working w 1 block to guess the key for that block
		print block
		if(len(block) % 2 == 1):
			block = block[1:]
		res_to_key = {}
		temp = []
		for i in range(0, 255):
			try:
				res = single_hex_xor(block.rstrip(), i)
				res_to_key[res] = key
				temp.append(res)
			except:
				pass
		list2 = sorted(temp, cmp = cos_compare)
		print list2
	#print keys"""
	for block in trans:
		res_to_key = {}
		temp = []
		print block
		for i in range(0, 255):
			res = single_hex_xor(block, i)
			res_to_key[res] = i
			temp.append(res)
		list2 = sorted(temp, cmp = cos_compare)
		keys.append(res_to_key[list2[len(list2) - 1]])
	print keys
	final_key = ""
	for key in keys:
		#print chr(key)
		final_key += chr(key)
	print final_key
	return final_key

#def bruteforce(string, n):
#	trans = transpose(string, n)
#	keys = []
final_key = bruteforce(ciphertext, g3)

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
	#print res.encode('hex')
	print res
	return res

print 'result:'

repeat_key_xor(ciphertext, final_key)