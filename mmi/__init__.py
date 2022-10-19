import hashlib
import os
import sys

BLOCKSIZE = 65536
homedir = os.path.expanduser('~')

if os.path.exists(homedir+'/.local/data/mmi.bloom') == True:
    __location__ = LOCATION = homedir+'/.local/data/mmi.bloom'
elif os.path.exists('/usr/local/data/mmi.bloom') == True:
    __location__ = LOCATION = '/usr/local/data/mmi.bloom'
else:
    path = os.path.dirname(__file__)
    __location__ = LOCATION = path[:-4]+'/data/mmi.bloom'

__emptyfile__ = EMPTYFILE = '\033[94m{}\033[00m'        ### PURPLE ###
__knownfile__ = KNOWNFILE = '\033[92m{}\033[00m'        ### GREEN ###
__knownmeta__ = KNOWNMETA = '\033[96m{}\033[00m'        ### BLUE ###
__largefile__ = LARGEFILE = '\033[91m{}\033[00m'        ### RED ###
__partialmeta__ = PARTIALMETA = '\033[97m{}\033[00m'    ### GREY ###
__sha256__ = SHA256 = 'EDF180207F677A829B53EBF23FAD4EBDA942D1C343AC8E0A9265AA24584D8528'
__version__ = VERSION = '3.0'

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