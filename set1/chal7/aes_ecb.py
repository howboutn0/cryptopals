from Crypto.Cipher import AES
import base64
key = 'YELLOW SUBMARINE'

decipher = AES.new(key, AES.MODE_ECB)

with open('file') as input_file:
	ciphertext = base64.b64decode(input_file.read())

print decipher.decrypt(ciphertext)