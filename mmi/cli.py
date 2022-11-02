import asyncio
import hashlib
import pathlib
import pybloomfilter
from mmi import __emptyfile__
from mmi import __gtfo__
from mmi import __knownfile__
from mmi import __knownmeta__
from mmi import __largefile__
from mmi import __location__
from mmi import __partialmeta__
from mmi import __version__

BLOCKSIZE = 65536

mmi = pybloomfilter.BloomFilter.open(str(__location__))
gtfo = pybloomfilter.BloomFilter.open(str(__gtfo__))

async def check(sha256):
    value = {}
    if sha256 in mmi:           ### MMI ###
        value['meta'] = 'YES'
    else:
        value['meta'] = 'NO'
    if sha256 in gtfo:          ### GTFO ###
        value['gtfo'] = 'YES'
    else:
        value['gtfo'] = 'NO'
    return value

async def hasher(fullpath):
    try:
        sha256_hasher = hashlib.sha256()
        with open(fullpath,'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                sha256_hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        sha256_file = sha256_hasher.hexdigest().upper()
    except:
        sha256_file = '                                                                '
        pass
    if sha256_file == 'E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855':
        sha256_file = __emptyfile__.format('** EMPTY **                                                     ')
    status = await check(sha256_file)
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

async def metahash(fullpath):
    sha256_meta = hashlib.sha256()
    sha256_meta.update(fullpath.encode())
    sha256_hash = sha256_meta.hexdigest().upper()
    status = await check(sha256_hash)
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

async def parsefilename(filename):
    if filename[:1] == '/':
        out = filename.split('/')
        count = len(out) - 1
        status = await metahash(out[count])
    return status

async def parseonlypath(onlypath):
    if onlypath[:1] == '/':
        out = onlypath.split('/')
        del out[-1]
        onlypath = '/'.join(out)
        status = await metahash(onlypath)
    return status

async def start():
    print('|---------------------------------------')
    print('| MatchMeta.Info v'+__version__+' (mmi) ')
    print('| - pip install matchmeta --upgrade     ')
    print('|---------------------------------------')
    for p in pathlib.Path.cwd().iterdir():
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
                value = await hasher(p)
                gtfo_hash = value['gtfo']
                sha256 = value['sha256']
        elif isDir == True:
            sha256 = ' -- DIR --                                                      '
        normalized = await normalize(str(p))
        fullpath = await metahash(normalized)
        if fullpath['gtfo'] == 'YES':
            gtfo_path = __largefile__.format('P')
        if fullpath['meta'] == 'YES':
            dir = __knownmeta__.format(str(p.parent))
            file = __knownmeta__.format(str(p.name))
            slash = __knownmeta__.format('/')
        elif fullpath['meta'] == 'NO':
            directory = await parseonlypath(normalized)
            if directory['meta'] == 'YES':
                dir = __partialmeta__.format(str(p.parent))
            else:
                dir = str(p.parent)
            filename = await parsefilename(normalized)
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

def main():
    asyncio.run(start())