# mmi

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

count = 0

with zipfile.ZipFile(output['filename']) as z:
	with z.open('matchmeta-unique-sha256.txt') as f:
		for line in f:
			value = line[:-1].decode().strip('"')
			if value != 'sha256':
				mmi.add(value)
				count += 1
	f.close()
z.close()

mmi.sync()

print(count)
```
