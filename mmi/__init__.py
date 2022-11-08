import hashlib
import pathlib
import sys

BLOCKSIZE = 65536

local = pathlib.Path.joinpath(pathlib.Path(__file__).resolve().parents[1],'data/mmi.bloom')
localgtfo = pathlib.Path.joinpath(pathlib.Path(__file__).resolve().parents[1],'data/gtfo.bloom')
user = pathlib.Path.joinpath(pathlib.Path.home(),'.local/data/mmi.bloom')
usergtfo = pathlib.Path.joinpath(pathlib.Path.home(),'.local/data/gtfo.bloom')
system = pathlib.Path('/usr/local/data/mmi.bloom')
systemgtfo = pathlib.Path('/usr/local/data/gtfo.bloom')

if user.is_file() == True:
    __location__ = LOCATION = user
    __gtfo__ = GTFO = usergtfo
elif system.is_file() == True:
    __location__ = LOCATION = system
    __gtfo__ = GTFO = systemgtfo
else:
    __location__ = LOCATION = local
    __gtfo__ = GTFO = localgtfo

__emptyfile__ = EMPTYFILE = '\033[94m{}\033[00m'        ### PURPLE ###
__knownfile__ = KNOWNFILE = '\033[92m{}\033[00m'        ### GREEN ###
__knownmeta__ = KNOWNMETA = '\033[96m{}\033[00m'        ### BLUE ###
__largefile__ = LARGEFILE = '\033[91m{}\033[00m'        ### RED ###
__partialmeta__ = PARTIALMETA = '\033[97m{}\033[00m'    ### GREY ###
__sha256__ = SHA256 = '95D88E4F3FCCFB6F3CD789E0B0B4EDE968BC9E4F9F391CEEDA10976564821BC4'
__sha256gtfo__ = SHA256GTFO = '33481050CE3F4C94FF8020481B4AF5547DD361BB716E566E80C0E25F8A8D0631'
__version__ = VERSION = '8.0'

sha256_hasher = hashlib.sha256()    ### MMI ###

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

sha256_hasher = hashlib.sha256()    ### GTFO ###

with open(__gtfo__,'rb') as f:
    buf = f.read(BLOCKSIZE)
    while len(buf) > 0:
        sha256_hasher.update(buf)
        buf = f.read(BLOCKSIZE)
f.close()

sha256_file = sha256_hasher.hexdigest().upper()

if sha256_file != __sha256gtfo__:
    print("GTFO bloom filter is corrupted.")
    sys.exit(1)