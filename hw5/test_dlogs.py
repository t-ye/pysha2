print('Testing dlogs...', end='\t')

from dlogs import dlog,babygiantstep,pohlighellman
dlog_tests = [
    (2,5,1,4), # dlog_2(1) = 0 in Z/5Z*
    (2,5,2,4), # dlog_2(2) = 1 in Z/5Z*
    (2,5,4,4), # dlog_2(4) = 2 in Z/5Z*
    (2,5,3,4), # dlog_2(3) = 3 in Z/5Z*
	(2,37,3,36), # dlog_2(3) = 26 in Z/37Z*
	(45,71,48,7) # dlog_2(3) = 26 in Z/37Z*
]

for (g,p,t,q) in dlog_tests :
	exp_dlog = dlog(g,p,t,q)
	exp_bsgs = babygiantstep(g,p,t,q)
	assert pow(g, exp_dlog, p) == t % p, (g,p,t,q,exp_dlog)
	assert pow(g, exp_bsgs, p) == t % p, (g,p,t,q,exp_bsgs)
#assert exp_dlog == exp, 'dlog: dlog_{g}({t}) = {exp_dlog} mod {p}, expected {exp}'.format(g=g,p=p,t=t,q=q,exp_dlog=exp_dlog,exp=exp)
#assert exp_bsgs == exp, 'dlog: bsgs_{g}({t}) = {exp_bsgs} mod {p}, expected {exp}'.format(g=g,p=p,t=t,q=q,exp_bsgs=exp_bsgs,exp=exp)

print('Done.')
print('Testing pohlighellman (requires crt)...', end='\t')

ph_tests = [
	(2,5,1,[4]), # dlog_2(1) = 0 in Z/5Z*
	(2,5,2,[4]), # dlog_2(2) = 1 in Z/5Z*
	(2,5,4,[4]), # dlog_2(4) = 2 in Z/5Z*
	(2,5,3,[4]), # dlog_2(3) = 3 in Z/5Z*
	(2,37,3,[4,9]), # dlog_2(3) = 26 in Z/37Z*
	(2,37,3,[4,9]), # dlog_2(3) = 26 in Z/37Z*
	(5,37,3,[4,9]), # dlog_5(3) = 34 in Z/37Z*
	(7,71,3,[2,5,7]),
	(53,71,25,[2,5,7]),
	(3,61,34,[2,5])
]

for (g,p,t,qfactors) in ph_tests :
	exp_ph = pohlighellman(g,p,t,qfactors)
	assert pow(g, exp_ph, p) == t % p, (g,p,t,qfactors,exp_ph)
	# assert exp_ph == exp, 'dlog: ph_{g}({t}) = {exp_ph} mod {p}, expected {exp}'.format(g=g,p=p,t=t,q=q,exp_ph=exp_ph,exp=exp)

print('Done.')
