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
__sha256__ = SHA256 = 'AFA2B38029C2F6C635FCBD822F7CB36C5AF7FD2A05CB36F8F1D85630A62AA6B7'
__sha256gtfo__ = SHA256GTFO = '441C51EFD286D4BA2900A089C13353A95ED42EB978887AB2CE209FB96947720C'
__sha256common__ = SHA256COMMON = 'EB4A463921F832E3FBE9E596F0FDCE5CC7211F499A86FE8946574F799460888A'
__version__ = VERSION = '15.0'

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
