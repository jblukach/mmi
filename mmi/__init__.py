import pathlib

__emptyfile__ = EMPTYFILE = '\033[94m{}\033[00m'        ### PURPLE ###
__knownfile__ = KNOWNFILE = '\033[92m{}\033[00m'        ### GREEN ###
__knownmeta__ = KNOWNMETA = '\033[96m{}\033[00m'        ### BLUE ###
__largefile__ = LARGEFILE = '\033[91m{}\033[00m'        ### RED ###
__nofilehash__ = NOFILEHASH = '\033[93m{}\033[00m'      ### YELLOW ###
__partialmeta__ = PARTIALMETA = '\033[97m{}\033[00m'    ### GREY ###

__gtfo__ = GTFO = pathlib.Path.joinpath(pathlib.Path.home(), 'gtfo.bloom')
__mmi__ = MMI = pathlib.Path.joinpath(pathlib.Path.home(), 'mmi.bloom')

__version__ = VERSION = '2023.5.28'