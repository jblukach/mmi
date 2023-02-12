# mmi

Amazon Linux default installation now starts with about **150k** directories and files. How do we know which files belong on a particular host during the tirage of the operating system?

Review enough systems; you start remembering all those Amazon Linux operating system artifacts. Just in time for new directories and filenames to be added to the mix or moved to other locations.

The ```mmi``` command line tool lists the current path’s directories files based on user access permission, which are color-coded to help reduce triage time.

![MatchMeta.Info CLI Output](MMI.png)

### Installation

```
pip install matchmeta
```

### Command Line

```
mmi
```

### Color Coded

- :purple_square: Empty File (purple)
- :green_square: Known File (green)
- :blue_square: Known Meta (blue)
- :red_square: Large File (red)
- :white_large_square: Partial Meta (grey)
- :black_large_square: Unknown (black)

### GTFOBins

- H for Known SHA256 Hash :red_square: (red)
- P for Known Full Path :red_square: (red)
- F for Known File Name :red_square: (red)

https://gtfobins.github.io

### Likelihood >= 5

- H for Known SHA256 Hash :blue_square: (blue)
- P for Known Full Path :blue_square: (blue)
- F for Known File Name :blue_square: (blue)

### Local Development

```
pip install pybloomfiltermmap3
python setup.py install --user
```

### Build Bloom Filter

```python
import pybloomfilter
import requests
import zipfile

headers = {'x-api-key': '<key>'}

r = requests.get('https://sha256.lukach.io/unique', headers = headers)

output = r.json()

d = requests.get(output['link'])

if d.status_code == 200:
    with open(output['filename'], 'wb') as f:
        f.write(d.content)
f.close()

mmi = pybloomfilter.BloomFilter(10000000, 0.001, 'mmi.bloom')
common = pybloomfilter.BloomFilter(5000000, 0.001, 'common.bloom')

count = 0
number = 0

with zipfile.ZipFile(output['filename']) as z:
	with z.open('matchmeta-unique-sha256.txt') as f:
		for line in f:
			value = line[:-1].decode().strip('"')
			parse = value.split('","')
			if parse[0] != 'sha256':
				mmi.add(parse[0])
				count += 1
				if int(parse[1]) >= 5:
					common.add(parse[0])
					number += 1

	f.close()
z.close()

mmi.sync()
common.sync()

print(count)
print(number)
```
