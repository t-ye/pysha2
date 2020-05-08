def pollardlambda(g, p, t, q, b, w, theta=8) :
	"""
	Find x = dlog_g(t) in Z/pZ*, given that is in [b, b+w].
	"""
	from itertools import count
	from math import sqrt

	# Size of domain of f (heuristic).
	#L = int(sqrt(w))
	L = 5

	# Psuedorandom function to walk on exponents.
	def f(TW) :
		# return 1
		return pow(2, TW % L)

	# Some suggested parameters discussed in Oorschot and Wiener.
	# Appears to be a birthday-like bound for success, around
	# 1 - e**(-theta).
	a = 1/(2*sqrt(theta))
	m = a * sqrt(w)

	N = int(m*theta) # Tame sequence iterations.
	MAX_WILD_ITERS = 10**5

	# Tame & wild sequence initial values.
	T = pow(g, b+w, p)
	W = t
	if W == T :
		return (b+w) % q

	# Compute Nth tame sequence element (lay the trap).
	dT = 0
	for i in range(N) :
		dT += f(T)
		T = (T * pow(g, f(T), p)) % p
	# T = g**(b+w+dT)

	# Find element in wild sequence equal to Nth tame element
	# and return the corresponding
	dW = 0
	for j in count() :
		dW += f(W)
		W = (W * pow(g, f(W), p)) % p
		if W == T :
			# W = t*g**dW
			return (b+w + dT - dW) % q
		if dW > w + dT :
			raise RuntimeError('Failure: ' + str((g,p,t,q,b,w)))

	raise RuntimeError('Discrete log not found: ' + str((g,p,t,q,b,w)))

def partial_pohlighellman(g, p, t, qfactors, B) :
	from utils import prod
	# from ntheory import modinv
	# from sage.all import Integers, factor

	# Get information about <g> as a subgroup of Z/pZ.
	#R = Integers(p)
	#g = R(g)
	#n = g.order()
	q = prod(qfactors)

	# Find the smooth part of q, z.
	# fs = dict(factor(n))
	smoothfactors = {q_**e for q_,e in qfactors.items() if q_**e <= B}
	z = prod(smoothfactors)


	# Do Pohlig-Hellman on the projection of g down to Z/zZ, so that we find a
	# relation V = x mod z. If x < z, then V = x mod n too; otherwise, x = Az +
	# V for some A to be determined.
	V = pohlighellman(pow(g, q//z, p) , p, pow(t, q//z, p), smoothfactors)

	# Hope V = x mod n.
	return V

	# Notice that 0 <= A <= x/z. In particular, the larger z is, the less work
	# we have to do to find A.

	# Compute g**V and y1 = y/gV = g^{Az}. Set h := g^z; then g^{Az} = h^A.
	# Then A = dlog_h(y1).
	#gV = pow(g, V, p)
	#y1 = y * gV**(-1)
