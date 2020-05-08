print('Testing ntheory...', end='\t')
from ntheory import gcd,modinv,egcd,crt

gcd_tests = [
    (1,1,1),
    (1,2,1),
    (2,2,2),
    (2,4,2),
    (3*5, 3*7, 3),
    (312, 182, 26)
]

for (a,b,d) in gcd_tests :
    assert gcd(a,b) == d
    x,y,d = egcd(a,b)
    assert x*a + y*b == d

modinv_tests = [
    (2,5), # 2*3 == 1 mod 5
    (2,6), # 2 is not invertible mod 6
    (5,6), # 5*5 == 1 mod 6
    (3,11), # 3*4 == 1 mod 11
	(321093,109239012)
]

for (a,m) in modinv_tests :
	x = modinv(a,m)
	assert (x == None and gcd(a,m) != 1) or a*x % m == 1

crt_tests = [
	([2,4,5],[3,5,7]),
	([2,4,5],[9,5,7]),
	([5,7,8,2],[11,26,17,19]),
	([0,7,0,2],[59,26,17,19]),
	([1], [2]),
	([0], [2]),
	([2], [3])
]

for (xs,ps) in crt_tests :
	z = crt(xs,ps)
	assert all(z % p == x % p for x,p in zip(xs,ps)), "Got {z} for residues {xs} and moduli {ps}".format(z=z,xs=xs,ps=ps)

print('Done.')
