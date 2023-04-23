import datetime
import hashlib
import pathlib
import sys
import requests

now = int(datetime.datetime.now().timestamp())
update = pathlib.Path('/tmp/mmi.lastupdate')

def calculate(item):
    BLOCKSIZE = 65536
    sha256_hasher = hashlib.sha256()
    with open('/tmp/'+item+'.bloom', 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    f.close()
    sha256 = sha256_hasher.hexdigest().upper()
    return sha256

def download(item):
    r = requests.get('https://static.matchmeta.info/'+item+'.bloom')
    if r.status_code == 200:
        with open('/tmp/'+item+'.bloom', 'wb') as f:
            f.write(r.content)
    else:
        print('FAILED: https://static.matchmeta.info/'+item+'.bloom')
        sys.exit(1)

def verify(item):
    r = requests.get('https://static.matchmeta.info/'+item+'.sha256')
    if r.status_code == 200:
        return r.text
    else:
        print('FAILED: https://static.matchmeta.info/'+item+'.sha256')
        sys.exit(1)

__version__ = VERSION = '2023.4.1'

__emptyfile__ = EMPTYFILE = '\033[94m{}\033[00m'        ### PURPLE ###
__knownfile__ = KNOWNFILE = '\033[92m{}\033[00m'        ### GREEN ###
__knownmeta__ = KNOWNMETA = '\033[96m{}\033[00m'        ### BLUE ###
__largefile__ = LARGEFILE = '\033[91m{}\033[00m'        ### RED ###
__nofilehash__ = NOFILEHASH = '\033[93m{}\033[00m'      ### YELLOW ###
__partialmeta__ = PARTIALMETA = '\033[97m{}\033[00m'    ### GREY ###

__gtfo__ = GTFO = pathlib.Path('/tmp/gtfo.bloom')
__mmi__ = MMI = pathlib.Path('/tmp/mmi.bloom')

if __gtfo__.is_file() == False:
    pathlib.Path(update).write_text(str(now + 3600))
    download('gtfo')
    sha256 = verify('gtfo')
    check = calculate('gtfo')
    if check != sha256:
        print('CORRUPTED: /tmp/gtfo.bloom')
        sys.exit(1)
else:
    checked = int(pathlib.Path(update).read_text())
    if now > checked:
        sha256 = verify('gtfo')
        check = calculate('gtfo')
        if check != sha256:
            download('gtfo')
            check = calculate('gtfo')
            if check != sha256:
                print('CORRUPTED: /tmp/gtfo.bloom')
                sys.exit(1)
        pathlib.Path(update).write_text(str(now + 3600))

if __mmi__.is_file() == False:
    pathlib.Path(update).write_text(str(now + 3600))
    download('mmi')
    sha256 = verify('mmi')
    check = calculate('mmi')
    if check != sha256:
        print('CORRUPTED: /tmp/mmi.bloom')
        sys.exit(1)
else:
    checked = int(pathlib.Path(update).read_text())
    if now > checked:
        sha256 = verify('gtfo')
        check = calculate('gtfo')
        if check != sha256:
            download('mmi')
            check = calculate('mmi')
            if check != sha256:
                print('CORRUPTED: /tmp/mmi.bloom')
                sys.exit(1)
        pathlib.Path(update).write_text(str(now + 3600))