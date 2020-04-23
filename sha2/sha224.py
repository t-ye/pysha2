#!/usr/bin/python
__author__ = 'Thomas Dixon'
__license__ = 'MIT'

from sha2.sha256 import sha256

def new(m=None):
    return sha224(m)

class sha224(sha256):
    _h = (0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939,
          0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4)
    _output_size = 7
    digest_size = 28
