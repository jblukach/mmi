import asyncio
import hashlib
import os
import pybloomfilter
from mmi import __emptyfile__
from mmi import __knownfile__
from mmi import __knownmeta__
from mmi import __largefile__
from mmi import __location__
from mmi import __partialmeta__
from mmi import __version__

BLOCKSIZE = 65536
mmi = pybloomfilter.BloomFilter.open(__location__)

async def check(sha256):
    if sha256 in mmi:
        value = 'YES'
    else:
        value = 'NO'
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
    if status == 'YES':
        sha256_file = __knownfile__.format(sha256_file)
    return sha256_file

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
    path = os.getcwd()
    listing = os.listdir(path)
    for list in listing:
        isFile = os.path.isfile(path+'/'+list)
        isDir = os.path.isdir(path+'/'+list)
        if isFile == True:
            try:
                size = os.path.getsize(path+'/'+list)
            except: 
                size = 0
                pass
            if size == 0:
                sha256 = __emptyfile__.format('** EMPTY **                                                     ')
            elif size > 104857599:
                sha256 = __largefile__.format('** LARGE **                                                     ')
            else:
                sha256 = await hasher(path+'/'+list)
        elif isDir == True:
            sha256 = ' -- DIR --                                                      '
        if path == '/':
            normalized = await normalize(path+list)
        else:
            normalized = await normalize(path+'/'+list)
        fullpath = await metahash(normalized)
        if fullpath == 'YES':
            dir = __knownmeta__.format(path)
            file = __knownmeta__.format(list)
            slash = __knownmeta__.format('/')
        elif fullpath == 'NO':
            directory = await parseonlypath(normalized)
            if directory == 'YES':
                dir = __partialmeta__.format(path)
            else:
                dir = path
            filename = await parsefilename(normalized)
            if filename == 'YES':
                file = __partialmeta__.format(list)
            else:
                file = list
            slash = '/'
        else:
            dir = path
            file = list
            slash = '/'

        if path == '/':
            print(sha256+' '+dir+file)
        else:
            print(sha256+' '+dir+slash+file)

def main():
    asyncio.run(start())