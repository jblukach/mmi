import argparse
import concurrent.futures
import hashlib
import pathlib
import pybloomfilter
import requests
import sys
from mmi import __emptyfile__
from mmi import __knownfile__
from mmi import __knownmeta__
from mmi import __largefile__
from mmi import __nofilehash__
from mmi import __partialmeta__
from mmi import __gtfo__
from mmi import __mmi__
from mmi import __version__

def check(sha256, mmi, gtfo):

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

def calculate(location):

    BLOCKSIZE = 65536
    sha256_hasher = hashlib.sha256()
    with open(location, 'rb') as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            sha256_hasher.update(buf)
            buf = f.read(BLOCKSIZE)
    f.close()
    sha256 = sha256_hasher.hexdigest().upper()
    return sha256

def download():

    if __gtfo__.is_file() == False:
        print('UPDATING: '+str(__gtfo__))
        gtfobloom()
        sha256 = gtfoverify()
        check = calculate(__gtfo__)
        if check != sha256:
            print('CORRUPTED: '+str(__gtfo__))
            sys.exit(1)
        else:
            print('VERIFIED: '+str(__gtfo__))
    else:
        sha256 = gtfoverify()
        check = calculate(__gtfo__)
        if check != sha256:
            print('UPDATING: '+str(__gtfo__))
            gtfobloom()
            check = calculate(__gtfo__)
            if check != sha256:
                print('CORRUPTED: '+str(__gtfo__))
                sys.exit(1)
            else:
                print('VERIFIED: '+str(__gtfo__))
        else:
            print('CURRENT: '+str(__gtfo__))

    if __mmi__.is_file() == False:
        print('UPDATING: '+str(__mmi__))
        mmibloom()
        sha256 = mmiverify()
        check = calculate(__mmi__)
        if check != sha256:
            print('CORRUPTED: '+str(__mmi__))
            sys.exit(1)
        else:
            print('VERIFIED: '+str(__mmi__))
    else:
        sha256 = mmiverify()
        check = calculate(__mmi__)
        if check != sha256:
            print('UPDATING: '+str(__mmi__))
            mmibloom()
            check = calculate(__mmi__)
            if check != sha256:
                print('CORRUPTED: '+str(__mmi__))
                sys.exit(1)
            else:
                print('VERIFIED: '+str(__mmi__))
        else:
            print('CURRENT: '+str(__mmi__))

def gtfobloom():

    r = requests.get('https://static.matchmeta.info/gtfo.bloom')
    if r.status_code == 200:
        with open(__gtfo__, 'wb') as f:
            print('SUCCESS: https://static.matchmeta.info/gtfo.bloom')
            f.write(r.content)
    else:
        print('FAILED: https://static.matchmeta.info/gtfo.bloom')
        sys.exit(1)

def gtfoverify():

    r = requests.get('https://static.matchmeta.info/gtfo.sha256')
    if r.status_code == 200:
        print('SUCCESS: https://static.matchmeta.info/gtfo.sha256')
        return r.text
    else:
        print('FAILED: https://static.matchmeta.info/gtfo.sha256')
        sys.exit(1)

def hasher(fullpath, mmi, gtfo):

    try:
        BLOCKSIZE = 65536
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
    status = check(sha256_file, mmi, gtfo)
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

def metahash(fullpath, mmi, gtfo):

    sha256_meta = hashlib.sha256()
    sha256_meta.update(fullpath.encode())
    sha256_hash = sha256_meta.hexdigest().upper()
    status = check(sha256_hash, mmi, gtfo)
    return status

def mmibloom():

    r = requests.get('https://static.matchmeta.info/mmi.bloom')
    if r.status_code == 200:
        with open(__mmi__, 'wb') as f:
            print('SUCCESS: https://static.matchmeta.info/mmi.bloom')
            f.write(r.content)
    else:
        print('FAILED: https://static.matchmeta.info/mmi.bloom')
        sys.exit(1)

def mmiverify():

    r = requests.get('https://static.matchmeta.info/mmi.sha256')
    if r.status_code == 200:
        print('SUCCESS: https://static.matchmeta.info/mmi.sha256')
        return r.text
    else:
        print('FAILED: https://static.matchmeta.info/mmi.sha256')
        sys.exit(1)

def normalize(path):

    if path[:1] == '/':
        out = path.split('/')
        try:
            if out[1] == 'home':            ### LINUX
                out[2] = 'user'
                path = '/'.join(out)
            elif out[1] == 'Users':         ### APPLE
                if out[2] != 'Shared':
                    out[2] = 'user'
                    path = '/'.join(out)
        except:
            pass
    return path

def parsefilename(filename, mmi, gtfo):

    if filename[:1] == '/':
        out = filename.split('/')
        count = len(out) - 1
        status = metahash(out[count], mmi, gtfo)
    return status

def parseonlypath(onlypath, mmi, gtfo):

    if onlypath[:1] == '/':
        out = onlypath.split('/')
        del out[-1]
        onlypath = '/'.join(out)
        status = metahash(onlypath, mmi, gtfo)
    return status

def start(skip):

    mmi = pybloomfilter.BloomFilter.open(str(__mmi__))      ### MMI ###
    gtfo = pybloomfilter.BloomFilter.open(str(__gtfo__))    ### GTFO ###

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
                    if skip == False:
                        value = hasher(p, mmi, gtfo)
                        gtfo_hash = value['gtfo']
                        sha256 = value['sha256']
                    else:
                        gtfo_hash = ' '
                        sha256 = '                                                                '
            elif isDir == True:
                sha256 = ' -- DIR --                                                      '
            normalized = normalize(str(p))
            fullpath = metahash(normalized, mmi, gtfo)
            if fullpath['gtfo'] == 'YES':
                gtfo_path = __largefile__.format('P')
            if fullpath['meta'] == 'YES':
                dir = __knownmeta__.format(str(p.parent))
                file = __knownmeta__.format(str(p.name))
                slash = __knownmeta__.format('/')
            elif fullpath['meta'] == 'NO':
                directory = parseonlypath(normalized, mmi, gtfo)
                if directory['meta'] == 'YES':
                    dir = __partialmeta__.format(str(p.parent))
                else:
                    dir = str(p.parent)
                filename = parsefilename(normalized, mmi, gtfo)
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

    parser = argparse.ArgumentParser(description='MMI - OS Triage for Anyone and Everyone')
    parser.add_argument('-d', '--download', help='Download Bloom Filters', action='store_true')
    parser.add_argument('-s', '--skip', help='Skip File Hashing', action='store_true')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    args = parser.parse_args()

    if args.download:
        download()
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(start, args.skip)