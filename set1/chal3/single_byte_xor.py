import binascii
import math
string = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

#string: input a hex string
#key: type = int. range from 0 to 255
def single_hex_xor(string, key):
	ascii_string = binascii.unhexlify(string)
	res = ""
	for char in ascii_string:
		res = res + chr(ord(char) ^ key)
	return res

for i in range(0, 255):
	print single_hex_xor(string, i)

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
	return dot(x, y)/(magn(x) * magn(y))

test = dictfreq("critics have said that his metamorphosis into an insect is merely a process by which his physical form represents the quality of the life he leads before the transformation. defend or refute this claim and be sure to address kafka's message in the story. be usre also to use ample textual evidence to support your arguments")

print test
print cos(test, freq)

def cos_compare(string1, string2):
	dict1 = dictfreq(string1)
	dict2 = dictfreq(string2)
	cos1 = cos(dict1, freq)
	cos2 = cos(dict2, freq)

	return cos1 - cos2

list = []

with open(file, 'r+') as file:
	for line in file.readlines():
		for i in range(0, 255):
			list.append(single_hex_xor(line, i))
print 'hello'
list2 = sorted(list, cmp=cos_compare)
for item in list2:
	print item
