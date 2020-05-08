# Pre-computed values.
P = 0x3cf2a66e5e175738c9ce521e68361676ff9c508e53b6f5ef1f396139cbd422d9f90970526fd8720467f17999a6456555dda84aa671376ddbe180902535266d383
Q_F = {
	2: 1, 7: 1, 11: 1, 31: 1, 41: 1, 397: 1, 2161: 1, 4441:1, 45413: 1, 386963:
	1, 5935879: 1, 151450661: 1, 3338699715979708151: 1,
	1298436385387243925649768952547982719612192893541025013655713795578945932943571347718520825904341:1
}
G = 2
Q = P-1 # Order of G.
Y = 48523720656106337214498629461027915366341359339336716715097391785892912972213523155142591698711484419232822327996367621240326762320354108252747891415832385

def try_decrypt(c, B) :
	from ref import parse_mpi
	from ntheory import modinv
	import base64
	from dlogs import partial_pohlighellman
	from Crypto.Cipher import AES

	data = base64.decodebytes(c)

	index = 0
	gk  , index = parse_mpi(data,index) # g**k.
	m_yk, index = parse_mpi(data,index) # m*y**k.

	k = partial_pohlighellman(G, P, gk, Q_F, B)
	# yk = pow(gk, x, p)
	# m = m_yk * modinv(yk, p) % p

	yk = pow(Y, k, P)
	m = m_yk * modinv(yk, P) % P

	iv = data[index : index+AES.block_size]
	index += AES.block_size
	ctxt = data[index:]

	# aeskey = int_to_binary(m)
	aeskey = int(m).to_bytes(16, 'big')
	cipher = AES.new(aeskey, AES.MODE_CBC, iv)

	return cipher.decrypt(ctxt)

def decrypt_fromfile(B,ctxtfilename='ref/hw5.pdf.enc.asc') :#,  keyfilename='key.pub') :
	with open(ctxtfilename, 'rb') as ctxtfile :
		ctxt = ctxtfile.read()

	return try_decrypt(ctxt, B)

def main() :
	ptxt = decrypt_fromfile(151450661)
	with open('ref/hw5.pdf', 'wb') as f :
		f.write(ptxt)

if __name__ == '__main__' :
	main()
