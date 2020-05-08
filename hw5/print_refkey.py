def main() :
	filename = 'refkey.pub'
	from ref import parse_public_key

	with open(filename, 'rb') as f :
		pubkey = parse_public_key(f.read())
		print(pubkey)

if __name__ == '__main__' :
	main()
