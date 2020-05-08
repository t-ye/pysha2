# Constants found specifically in this homework. They are given precomputed here
# mainly so that we don't have to rely on Sage or other number theory libraries.
# Not everyone has Sage 9, and it would be massively inconvienent to install it
# just to run / grade this homework.

# ELGamal modulus.
P = 0x3cf2a66e5e175738c9ce521e68361676ff9c508e53b6f5ef1f396139cbd422d9f90970526fd8720467f17999a6456555dda84aa671376ddbe180902535266d383
# Group element of Z/pZ* generating a cyclic subgroup.
G = 2

# Order of G. (In general the order of G *divides* P-1. Here we are lucky.)
Q = P-1

# Factorization of Q into primes.
Q_factorization = {
	2: 1, 7: 1, 11: 1, 31: 1, 41: 1, 397: 1, 2161: 1, 4441:1, 45413: 1, 386963:
	1, 5935879: 1, 151450661: 1, 3338699715979708151: 1,
	1298436385387243925649768952547982719612192893541025013655713795578945932943571347718520825904341:1
}

# A random element in the cyclic subgroup of G.
Y = 48523720656106337214498629461027915366341359339336716715097391785892912972213523155142591698711484419232822327996367621240326762320354108252747891415832385

# Maximum group order for which it is tolerable to compute discrete logs.
SMOOTH_BOUND = 2**32

# Name of ciphertext file to decrypt.
CTXT_FILENAME = 'hw5.pdf.enc.asc'
