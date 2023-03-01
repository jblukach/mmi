import hashlib
import pathlib
import sys

BLOCKSIZE = 65536

local = pathlib.Path.joinpath(pathlib.Path(__file__).resolve().parents[1],'data/mmi.bloom')
localgtfo = pathlib.Path.joinpath(pathlib.Path(__file__).resolve().parents[1],'data/gtfo.bloom')
localcommon = pathlib.Path.joinpath(pathlib.Path(__file__).resolve().parents[1],'data/common.bloom')
user = pathlib.Path.joinpath(pathlib.Path.home(),'.local/data/mmi.bloom')
usergtfo = pathlib.Path.joinpath(pathlib.Path.home(),'.local/data/gtfo.bloom')
usercommon = pathlib.Path.joinpath(pathlib.Path.home(),'.local/data/common.bloom')
system = pathlib.Path('/usr/local/data/mmi.bloom')
systemgtfo = pathlib.Path('/usr/local/data/gtfo.bloom')
systemcommon = pathlib.Path('/usr/local/data/common.bloom')

if user.is_file() == True:
    __location__ = LOCATION = user
    __gtfo__ = GTFO = usergtfo
    __common__ = COMMON = usercommon
elif system.is_file() == True:
    __location__ = LOCATION = system
    __gtfo__ = GTFO = systemgtfo
    __common__ = COMMON = systemcommon
else:
    __location__ = LOCATION = local
    __gtfo__ = GTFO = localgtfo
    __common__ = COMMON = localcommon

__emptyfile__ = EMPTYFILE = '\033[94m{}\033[00m'        ### PURPLE ###
__knownfile__ = KNOWNFILE = '\033[92m{}\033[00m'        ### GREEN ###
__knownmeta__ = KNOWNMETA = '\033[96m{}\033[00m'        ### BLUE ###
__largefile__ = LARGEFILE = '\033[91m{}\033[00m'        ### RED ###
__partialmeta__ = PARTIALMETA = '\033[97m{}\033[00m'    ### GREY ###
__sha256__ = SHA256 = 'A29BA2FB5343992FCF588641AB622BB7D7E1FF04747A24EE403AE7BF42327472'
__sha256gtfo__ = SHA256GTFO = '8EC45F6C55984B66BE709611C689F0C63E2E44B68F55891BF7F300BAE4A56080'
__sha256common__ = SHA256COMMON = 'B2424267BB9C62A7850828955BDF6EE98C520BBAE195F495BA1862F8A0DE0C48'
__version__ = VERSION = '16.1'

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

sha256_hasher = hashlib.sha256()    ### COMMON ###

with open(__common__,'rb') as f:
    buf = f.read(BLOCKSIZE)
    while len(buf) > 0:
        sha256_hasher.update(buf)
        buf = f.read(BLOCKSIZE)
f.close()

sha256_file = sha256_hasher.hexdigest().upper()

if sha256_file != __sha256common__:
    print("COMMON bloom filter is corrupted.")
    sys.exit(1)
