def expcount(base, modulus=None, coeff=1) :
    """
    Yield coeff, coeff*base, coeff*(base**2), ...
    """
    if modulus != None :
        exp = coeff % modulus
    else :
        exp = coeff
    while True :
        yield exp
        if modulus != None :
            exp = (exp * base) % modulus
        else :
            exp = exp * base

def isqrt(n) :
	from math import sqrt
	return int(round(sqrt(n)))

def prod(itr, start=1) :
    """
    Compute product between all elements of an iterable.
    """
    val = start
    for el in itr :
        val *= el
    return val
