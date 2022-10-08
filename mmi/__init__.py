import hashlib
import os
import sys

BLOCKSIZE = 65536
path = os.path.dirname(__file__)

__emptyfile__ = EMPTYFILE = '\033[94m{}\033[00m' ### PURPLE ###
__knownfile__ = KNOWNFILE = '\033[92m{}\033[00m' ### GREEN ###
__knownmeta__ = KNOWNMETA = '\033[96m{}\033[00m' ### BLUE ###
__largefile__ = LARGEFILE = '\033[91m{}\033[00m' ### RED ###
__location__ = LOCATION = path[:-4]+'/data/mmi.bloom'
__partialmeta__ = PARTIALMETA = '\033[97m{}\033[00m' ### GREY ###
__sha256__ = SHA256 = '0754EDF87A433AD0970C9EBB3CFD40F28390389FD9FF172FEB1AE6445E7701C4'
__version__ = VERSION = '0'

sha256_hasher = hashlib.sha256()
with open(__location__,'rb') as f:
    buf = f.read(BLOCKSIZE)
    while len(buf) > 0:
        sha256_hasher.update(buf)
        buf = f.read(BLOCKSIZE)
f.close()

sha256_file = sha256_hasher.hexdigest().upper()

if sha256_file != __sha256__:
    print("MMI bloom filter is corrupted.")
    sys.exit(1)