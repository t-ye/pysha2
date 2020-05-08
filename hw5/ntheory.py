
def order(g,p) :
	from sage.all import Integers

	R = Integers(p)
	return R(g).multiplicative_order()


def _gcd(a,b) :
    if b == 0 :
        return a
    return _gcd(b, a%b)

def gcd(*args) :
    g = 0
    for arg in args :
        g = _gcd(arg, g)
        if g == 1 :
            break
    return g

def egcd(a,b) :
    if b == 0 :
        return (1,0,a)
    # q = a//b, r = a%b, so a = qb + r.
    (q,r) = divmod(a,b)

    # xb + yr = d, where d = gcd(b,r) = gcd(a,b).
    (x,y,d) = egcd(b,r)

    # xb + y(a-qb) = d
    # ya + (x-yq)b = d.
    return (y, x-y*q, d)

def modinv(a,m) :
    """
    Compute x such that ax = 1 (mod m). Returns None if no such b exists.
    """

    x,y,d = egcd(a,m)
    if d != 1 : return None
    return x % m


def _check_crt(xs,ps) :
	assert len(xs) == len(ps)
	#assert all(x % p != 0 for x,p in zip(xs,ps))

def crt(xs,ps) :
	"""
	Given list ps of coprime residues, and list xs where xs[i] is a residue
	mod ps[i], find z (mod prod(ps)) such that z = xs[i] mod ps[i] over all i.
	"""
	from utils import prod

	if len(xs) != len(ps) :
		raise ValueError(
			'Number of residues different from number of moduli: ' + \
			str(len(xs)) + ', ' + str(len(ps))
		)

	if len(ps) == 1 :
		return xs[0] % ps[0]

	if gcd(*ps) != 1 : raise ValueError('Moduli not coprime: ' + str(ps))

	n = len(xs)

	# Formally, z lives in Z/PZ.
	P = prod(ps)
	Ns = [ P//ps[i] for i in range(n)]

	z = 0
	for (x,p,N) in zip(xs, ps, Ns) :
		# rN = 1 mod p
		r = modinv(N, p)
		# if r == None : raise ValueError('ps not coprime: ' + str(ps))

		# By construction, rNx = x mod p and, of course, rNx = 0 mod N
		# which implies rNx = 0 mod p' for all p' != p.
		z += r*N*x

	return z % P

def _factor(n) :
	"""
	Hand-rolled integer prime factorization using wheel factorization:
	https://en.wikipedia.org/wiki/Wheel_factorization

	Let P be the product of some of the first few primes, e.g. P = 2*3*5 = 30.
	The algorithm is based on the observation that a number is prime only if
	either it is one of 2, 3, or 5, or its residue in Z/PZ is coprime to all of
	2, 3, or 5 (in other words, its residue is a prime not equalling 2, 3, and 5).

	In the most elementary case, we use P = 2, where we iterate over only odd
	numbers between 3 and sqrt(n). Here we only have to perform trial division
	against 50% of the integers between 1 and sqrt(n); when P = 2*3 = 6, it
	turns out we need to do trial division against ~34% of the integers in the same set.
	"""
	from collections import Counter
	from itertools import count
	from math import isqrt

	multiplicities = Counter()

	if n <= 0 : return ValueError("Trying to factor nonpositive integer: " + str(n))

	while n % 2 == 0 :
		multiplicities[2] += 1
		n //= 2

	while n % 3 == 0 :
		multiplicities[3] += 1
		n //= 3

	# The "prime residues" mod 2*3 = 6 are 1 and 5. That is, with the exception
	# of 2 and 3, only the integers in the sets 6Z + 1 and 6Z + 5 are possibly
	# prime; the integers in the other sets are not.

	for z in count(0, 6) : # 6, 12, 18, ...
		if z*z > n :
			break

		if z != 0 :
			while n % (z+1) == 0 :
				multiplicities[z+1] += 1
				n //= z+1

		while n % (z+5) == 0 :
			multiplicities[z+5] += 1
			n //= z+5

	if n != 1 : multiplicities[n] += 1
	return multiplicities

def factor(n) :
	# For small n, use hand-rolled factoring algorithm to avoid slow imports.
	if n <= 2**16 :
		return _factor(n)

	from sage.all import factor

	return factor(n)
