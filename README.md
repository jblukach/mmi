# :construction: mmi :construction:

## :crab: Rust Migration :crab:

Metadata is the lowest-value indicator as easy to circumvent. Still, with the exponential volume of directories and files standard on default operating system installations, finding things hiding in plain sight has become an important analysis technique.

```
MMI - OS Triage for Anyone and Everyone

options:
  -h, --help      show this help message and exit
  -d, --download  Download Bloom Filters
  -s, --skip      Skip File Hashing
  -u, --updated   Bloom Filters Last Updated
  -v, --version   show program's version number and exit
  ```

### DATASET

GetBlocks generates the dataset using the SHA256 format for directories, files, hashes, and paths.

https://github.com/4n6ir/getblocks

A pipeline runs every hour to determine if AWS has released any new verified Amazon Machine Image (AMI) to harvest artifacts.

### DISTRIBUTION

A download option in the command line interface (CLI) stores the bloom filters in the user's home directory.

```
mmi -d
```

Please use these links to download the bloom filters for offline analysis.

https://dl.4n6ir.com/match-meta-info/gtfo.bloom

https://dl.4n6ir.com/match-meta-info/mmi.bloom

You can verify the integrity of the bloom filters by using the provided SHA256 hash values.

https://dl.4n6ir.com/match-meta-info/gtfo.sha256

https://dl.4n6ir.com/match-meta-info/mmi.sha256

Raw data is available for download if you want to use the artifacts elsewhere.

https://dl.4n6ir.com/?p=amazon-linux-pipeline/

### LAST UPDATED

Check when the bloom filters were last updated using the command line interface (CLI).

```
mmi -u
```

Or by hitting the provided website for the last updated timestamp.

https://dl.4n6ir.com/match-meta-info/last.updated

### COUNTS

https://dl.4n6ir.com/match-meta-info/gtfo.count

https://dl.4n6ir.com/match-meta-info/mmi.count

### DETECTIONS

:purple_square: Empty File (purple) 

A zero byte size determines empty files or the following hash value for this detection.

```E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855```

:green_square: Known File (green)

The SHA256 hash value for the specific file contents matches one found on an operating system in the dataset.

:blue_square: Known Meta (blue)

The full path matches precisely to one found on an operating system in the dataset.

:red_square: Large File (red)

A 100 MB or more gets marked as a large file to maintain application performance.

:yellow_square: Not Available (yellow)

If something goes wrong during the hashing of the file content, the program lets you know that the hash is unavailable.

:white_large_square: Partial Meta (grey)

If only the directory or filename matches, it indicates a familiar name from the dataset.

:black_large_square: Unknown (black)

Default color coding without any detections available from the dataset.

### GTFOBINS

GTFOBins is a curated list of Unix binaries that can bypass local security restrictions in misconfigured systems.

https://gtfobins.github.io

Identifying files that provide the ability to live off the land is essential.

```H``` for Known SHA256 Hash :red_square: (red)

```P``` for Known Full Path :red_square: (red)

```F``` for Known File Name :red_square: (red)

### ACCESS DENIED

Three stars ```***``` :red_square: (red) indicate that you do not have access to hash the contents of a specific file.

### INSTALLATION

```
pip install matchmeta
```

### DEVELOPMENT

```
python setup.py install --user
```

![Match Meta Inforamtion (MMI)](images/mmi.png)
