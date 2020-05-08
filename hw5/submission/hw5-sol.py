from constants import P, G, Q, Q_factorization, Y, SMOOTH_BOUND, CTXT_FILENAME
import struct

# Copied from reference code.
# Read one MPI-formatted value beginning at s[index]
# Returns value and index + bytes read.
def parse_mpi(s,index):
    length = struct.unpack('<I',s[index:index+4])[0]
    # z = Integer(s[index+4:index+4+length].hex(),16)
    z = int(s[index+4:index+4+length].hex(),16)
    return z, index+4+length

def trydecrypt(ctxt : list, B : int) -> bytes :
	"""
	Try to decrypt ctxt by solving the discrete logarithm problem in a subgroup
	of B-smooth order. If the ElGamal exponent k is small enough, and B is large
	enough then this will be equivalent to finding k in the overall group.
	"""
	from ntheory import modinv
	import base64
	from dlogs import partial_pohlighellman
	from Crypto.Cipher import AES

	# Remove header and footer delineations, and strip trailing newline
	ctxt = b''.join(ctxt[1:-1])
	data = base64.decodebytes(ctxt) # base 64 to bytes

	index = 0
	gk  , index = parse_mpi(data,index) # G**k.
	m_yk, index = parse_mpi(data,index) # m*Y**k.

	# ElGamal encryption is broken if we can recover k, i.e. can compute
	# Dlog_G(gk) in Z/PZ*. We can try projecting G and gk down to a subgroup of
	# <G> of B-smooth order, and solve the discrete log problem there, using the
	# Pohlig-Hellman decomposition.

	Q_primepows = [q_**e for q_,e in Q_factorization.items()]
	k = partial_pohlighellman(G, P, gk, Q_primepows, B)

	# Given k, can recover m - the symmetric key.
	yk = pow(Y, k, P)
	m = m_yk * modinv(yk, P) % P

	iv     = data[index                : index+AES.block_size]
	encmsg = data[index+AES.block_size :                     ]

	# aeskey = int_to_binary(m)
	aeskey = int(m).to_bytes(16, 'big') # Big-endian
	cipher = AES.new(aeskey, AES.MODE_CBC, iv)

	return cipher.decrypt(encmsg) # Hopefully this is it!

def trydecrypt_fromfile(B : int, ctxtfilename : str) -> bytes :
	with open(ctxtfilename, 'rb') as ctxtfile :
		ctxt = ctxtfile.readlines()

	return trydecrypt(ctxt, B)

def main() :
	"""
	Given SMOOTH_BOUND, an upper bound for group orders for which the discrete
	logarithm is tractable, try to recover the plaintext using the given
	ciphertext and ElGamal public key.
	"""
	ptxt = trydecrypt_fromfile(SMOOTH_BOUND, CTXT_FILENAME)
	with open('hw5.pdf', 'wb') as f :
		f.write(ptxt)

if __name__ == '__main__' :
	main()
