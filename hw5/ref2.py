#!/usr/bin/env sage

from sage.all import *
import struct
import re
from Crypto.Cipher import AES
from Crypto import Random

key_header = '-----BEGIN PRETTY BAD PUBLIC KEY BLOCK-----\n'
key_footer = '-----END PRETTY BAD PUBLIC KEY BLOCK-----\n'

PRIME = 0x3cf2a66e5e175738c9ce521e68361676ff9c508e53b6f5ef1f396139cbd422d9f90970526fd8720467f17999a6456555dda84aa671376ddbe180902535266d383
PRIME_FACTORIZATION = {
	2: 1, 7: 1, 11: 1, 31: 1, 41: 1, 397: 1, 2161: 1, 4441:1, 45413: 1, 386963:
	1, 5935879: 1, 151450661: 1, 3338699715979708151: 1,
	1298436385387243925649768952547982719612192893541025013655713795578945932943571347718520825904341:1
}


# Generate ElGamal public key (p,g,y=g^x mod p) in standardized PBP Diffie-Hellman group
def gen_public_key():
	import base64
	p = 0x3cf2a66e5e175738c9ce521e68361676ff9c508e53b6f5ef1f396139cbd422d9f90970526fd8720467f17999a6456555dda84aa671376ddbe180902535266d383
	R = Integers(p)
	g = R(2)
	#x = ZZ.random_element(2**128)
	x = 2**64 # For testing purposes.
	y = g**x

	key = int_to_mpi(p)+int_to_mpi(g)+int_to_mpi(y)
	key = base64.encodestring(key)

	return key_header + key + key_footer

# Our "MPI" format consists of 4-byte integer length l followed by l bytes of binary key
def int_to_mpi(z):
	s = int_to_binary(z)
	return struct.pack('<I',len(s))+s

# Horrible hack to get binary representation of arbitrary-length long int
def int_to_binary(z):
	s = ("%x"%z); s = (('0'*(len(s)%2))+s).decode('hex')
	return s

# Read one MPI-formatted value beginning at s[index]
# Returns value and index + bytes read.
def parse_mpi(s,index):
	length = struct.unpack('<I',s[index:index+4])[0]
	z = Integer(s[index+4:index+4+length].encode('hex'),16)
	return z, index+4+length

# An ElGamal public key consists of a magic header and footer enclosing the MPI-encoded values for p, g, and y.
def parse_public_key(s):
	data = re.search(key_header+"(.*)"+key_footer,s,flags=re.DOTALL).group(1) #.decode('base64')
	data = data.decode('base64')
	index = 0
	p,index = parse_mpi(data,index)
	g,index = parse_mpi(data,index)
	y,index = parse_mpi(data,index)
	return {'p':p, 'g':g, 'y':y}

encrypt_header = '-----BEGIN PRETTY BAD ENCRYPTED MESSAGE-----\n'
encrypt_footer = '-----END PRETTY BAD ENCRYPTED MESSAGE-----\n'

# PKCS 7 pad message.
def pad(s,blocksize=AES.block_size):
	n = blocksize-(len(s)%blocksize)
	return s+chr(n)*n

# Encrypt string s using ElGamal encryption with AES in CBC mode.
# Generate a 128-bit symmetric key, encrypt it using ElGamal, and prepend the MPI-encoded ElGamal ciphertext to the AES-encrypted ciphertext of the message.
def encrypt(pubkey,s):
	p = pubkey['p']; R = Integers(p)
	g = R(pubkey['g']); y = R(pubkey['y'])
	k = ZZ.random_element(2**128)
	m = 2**32 # ZZ.random_element(2**128) # For testing purposes.

	output = int_to_mpi(g**k)+int_to_mpi(m*(y**k))

	aeskey = int_to_binary(m)
	aeskey = bytes(16-len(aeskey)) + aeskey
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(aeskey, AES.MODE_CBC, iv)

	output += iv + cipher.encrypt(pad(s))

	return encrypt_header + output.encode('base64') + encrypt_footer

def main() :
	f = open("key.pub",'w')
	f.write(gen_public_key())
	f.close()

	plaintext = open('hw5.pdf').read()
	pubkey = parse_public_key(open('key.pub').read())
	print(pubkey)
	f = open('hw5.pdf.enc.asc','w')
	f.write(encrypt(pubkey,plaintext))
	f.close()

if __name__=='__main__':
        main()
