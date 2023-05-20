import asyncio
import datetime
import hashlib
import pathlib
import pybloomfilter
import sys
import requests
from mmi import __emptyfile__
from mmi import __gtfo__
from mmi import __knownfile__
from mmi import __knownmeta__
from mmi import __largefile__
from mmi import __mmi__
from mmi import __nofilehash__
from mmi import __partialmeta__
from mmi import __version__

BLOCKSIZE = 65536

now = int(datetime.datetime.now().timestamp())
update = pathlib.Path('/tmp/mmi.lastupdate')

async def calculate(item):
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

async def check(sha256, mmi, gtfo):
    value = {}
    if sha256 in mmi:
        value['meta'] = 'YES'
    else:
        value['meta'] = 'NO'
    if sha256 in gtfo:
        value['gtfo'] = 'YES'
    else:
        value['gtfo'] = 'NO'
    return value

async def download(item):
    r = requests.get('https://static.matchmeta.info/'+item+'.bloom')
    if r.status_code == 200:
        with open('/tmp/'+item+'.bloom', 'wb') as f:
            f.write(r.content)
    else:
        print('FAILED: https://static.matchmeta.info/'+item+'.bloom')
        sys.exit(1)

async def hasher(fullpath, mmi, gtfo):
    try:
        sha256_hasher = hashlib.sha256()
        with open(fullpath,'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                sha256_hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        sha256_file = sha256_hasher.hexdigest().upper()
    except:
        sha256_file = __nofilehash__.format('** N/A **                                                       ')
        pass
    if sha256_file == 'E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855':
        sha256_file = __emptyfile__.format('** EMPTY **                                                     ')
    status = await check(sha256_file, mmi, gtfo)
    if status['meta'] == 'YES':
        sha256_file = __knownfile__.format(sha256_file)
    if status['gtfo'] == 'YES':
        gtfo_hash = __largefile__.format('H')
    else:
        gtfo_hash = ' '
    value = {}
    value['sha256'] = sha256_file
    value['gtfo'] = gtfo_hash
    return value

async def metahash(fullpath, mmi, gtfo):
    sha256_meta = hashlib.sha256()
    sha256_meta.update(fullpath.encode())
    sha256_hash = sha256_meta.hexdigest().upper()
    status = await check(sha256_hash, mmi, gtfo)
    return status

async def normalize(path):
    if path[:1] == '/':
        out = path.split('/')
        try:
            if out[1] == 'home':
                out[2] = 'user'
                path = '/'.join(out)
        except:
            pass
    return path

async def parsefilename(filename, mmi, gtfo):
    if filename[:1] == '/':
        out = filename.split('/')
        count = len(out) - 1
        status = await metahash(out[count], mmi, gtfo)
    return status

async def parseonlypath(onlypath, mmi, gtfo):
    if onlypath[:1] == '/':
        out = onlypath.split('/')
        del out[-1]
        onlypath = '/'.join(out)
        status = await metahash(onlypath, mmi, gtfo)
    return status

async def verify(item):
    r = requests.get('https://static.matchmeta.info/'+item+'.sha256')
    if r.status_code == 200:
        return r.text
    else:
        print('FAILED: https://static.matchmeta.info/'+item+'.sha256')
        sys.exit(1)

async def start():

    if __gtfo__.is_file() == False:
        pathlib.Path(update).write_text(str(now + 3600))
        await download('gtfo')
        sha256 = await verify('gtfo')
        check = await calculate('gtfo')
        if check != sha256:
            print('CORRUPTED: /tmp/gtfo.bloom')
            sys.exit(1)
    else:
        checked = int(pathlib.Path(update).read_text())
        if now > checked:
            sha256 = await verify('gtfo')
            check = await calculate('gtfo')
            if check != sha256:
                await download('gtfo')
                check = await calculate('gtfo')
                if check != sha256:
                    print('CORRUPTED: /tmp/gtfo.bloom')
                    sys.exit(1)
            pathlib.Path(update).write_text(str(now + 3600))

    if __mmi__.is_file() == False:
        pathlib.Path(update).write_text(str(now + 3600))
        await download('mmi')
        sha256 = await verify('mmi')
        check = await calculate('mmi')
        if check != sha256:
            print('CORRUPTED: /tmp/mmi.bloom')
            sys.exit(1)
    else:
        checked = int(pathlib.Path(update).read_text())
        if now > checked:
            sha256 = await verify('mmi')
            check = await calculate('mmi')
            if check != sha256:
                await download('mmi')
                check = await calculate('mmi')
                if check != sha256:
                    print('CORRUPTED: /tmp/mmi.bloom')
                    sys.exit(1)
            pathlib.Path(update).write_text(str(now + 3600))

    mmi = pybloomfilter.BloomFilter.open(str(__mmi__))      ### MMI ###
    gtfo = pybloomfilter.BloomFilter.open(str(__gtfo__))    ### GTFO ###

    print('|---------------------------------------')
    print('| MatchMeta.Info v'+__version__+' (mmi) ')
    print('|---------------------------------------')

    for p in pathlib.Path.cwd().iterdir():
        try:
            gtfo_file = ' '
            gtfo_hash = ' '
            gtfo_path = ' '
            isFile = p.is_file()
            isDir = p.is_dir()
            if isFile == True:
                try:
                    size = pathlib.Path(p).stat().st_size
                except: 
                    size = 0
                    pass
                if size == 0:
                    sha256 = __emptyfile__.format('** EMPTY **                                                     ')
                elif size > 104857599:
                    sha256 = __largefile__.format('** LARGE **                                                     ')
                else:
                    value = await hasher(p, mmi, gtfo)
                    gtfo_hash = value['gtfo']
                    sha256 = value['sha256']
            elif isDir == True:
                sha256 = ' -- DIR --                                                      '
            normalized = await normalize(str(p))
            fullpath = await metahash(normalized, mmi, gtfo)
            if fullpath['gtfo'] == 'YES':
                gtfo_path = __largefile__.format('P')
            if fullpath['meta'] == 'YES':
                dir = __knownmeta__.format(str(p.parent))
                file = __knownmeta__.format(str(p.name))
                slash = __knownmeta__.format('/')
            elif fullpath['meta'] == 'NO':
                directory = await parseonlypath(normalized, mmi, gtfo)
                if directory['meta'] == 'YES':
                    dir = __partialmeta__.format(str(p.parent))
                else:
                    dir = str(p.parent)
                filename = await parsefilename(normalized, mmi, gtfo)
                if filename['gtfo'] == 'YES' and isFile == True:
                    gtfo_file = __largefile__.format('F')
                if filename['meta'] == 'YES':
                    file = __partialmeta__.format(str(p.name))
                else:
                    file = str(p.name)
                slash = '/'
            else:
                dir = str(p.parent)
                file = str(p.name)
                slash = '/'

            if str(p.parent) == '/':
                print(gtfo_hash+gtfo_path+gtfo_file+' '+sha256+' '+dir+file)
            else:
                print(gtfo_hash+gtfo_path+gtfo_file+' '+sha256+' '+dir+slash+file)

        except PermissionError:

            denied = __largefile__.format('***')
            sha256 = __nofilehash__.format('** N/A **                                                       ')
            dir = __largefile__.format(str(p.parent))
            file = __largefile__.format(str(p.name))
            slash = __largefile__.format('/')

            if str(p.parent) == '/':
                print(denied+' '+sha256+' '+dir+file)
            else:
                print(denied+' '+sha256+' '+dir+slash+file)

def main():
    asyncio.run(start())
