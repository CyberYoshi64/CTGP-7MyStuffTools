# CTGP-7 MyStuff Tools

## Tools

### `convertToChpack.py`

```
usage: convertToChpack.py [-h] [-r dir] [-m dir] [-v] [-o OUTPUT] [-d] [-b] [-c] [characters ...]

positional arguments:
  characters            If specified, only convert specified characters

options:
  -h, --help            show this help message and exit
  -r dir, --root dir    Alternative CTGP-7 root, defaults to standard Citra install
  -m dir, --mystpath dir
                        Alternative MyStuff root, default is '(root)/MyStuff/Characters'
  -v, --verbose         Output exactly what's being done
  -o OUTPUT, --output OUTPUT
                        Output path; for multiple characters, use '{}'.
  -d, --dir             Output path is a folder
  -b, --bclimtool       [Experiment] Modify bad BCLIM's using 'bclimtool' (https://github.com/dnasdw/bclimtool)
  -c, --compress, --combine-dup
                        Merge files with duplicate data
```

### `sarctool.py`

```
usage: sarctool.py [-h] [--saht SAHT] [--mergedup] [--no-sfnt] [--align int] [-u] [-c] [-x] [-v] [--saht-append out] sarc dir

positional arguments:
  sarc               SARC file
  dir                Directory or other SARC

options:
  -h, --help         show this help message and exit
  --saht SAHT        SARC Hash Table to use incase of missing SFNT data
  --mergedup         Merge duplicate data
  --no-sfnt          Do not add file names in SFNT
  --align int        Force custom alignment

Mode:
  -u, --update       Update files to SARC
  -c, --create       Delete SARC beforehand if it exists
  -x, --extract      Extract SARC to directory
  -v, --verbose      Say a lot that's done
  --saht-append out  Append entries to SAHT when updating files in SARC
```

### `saht.py`

```
usage: saht.py [-h] [-s file] [-t file] [-o file] [-y type] [-x] [-a] [-c] [-r] [-p] [keys ...]

positional arguments:
  keys

options:
  -h, --help            show this help message and exit
  -s file, --saht file  SAHT file
  -t file, --text file  Text file containing keys
  -o file, --output file
                        Output file (.saht/.txt)
  -y type, --verify type
                        'remove'/'fix' bad keys in SAHT
  -x, --extract         Extract keys from SAHT
  -a, --append          Append keys to SAHT
  -c, --create          Create SAHT from keys
  -r, --remove          Remove keys from SAHT
  -p, --print           List SAHT keys
```

### `sahtappend.py`

Side-thing - unsure whether to actually finish it

### `readchpack.py`

Simply reads a chpack and extracts some info - nothing fancy

### `ioHelper.py`

A module to help write files - it's not a program - have to move it somewhere else to not clash it against the actual tools

