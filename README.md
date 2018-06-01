Keep your files encodings consistent [![Build Status](https://travis-ci.org/B3QL/pep263.svg?branch=master)](https://travis-ci.org/B3QL/pep263)
====================================
Command line tool for managing source files encodings based on PEP263.

Instalation
===========
`pip install pep263`

Usage
=====
Help
----
```commandline
$ pep263 --help
Usage: pep263 [OPTIONS] [PATH]

  Manage source files encodings.

Options:
  --version          Show the version and exit.
  -A, --append TEXT  Append encoding to files
  -f, --force        Overwrite all files encoding
  --help             Show this message and exit.

```
Listing encodings
-----------------------
```commandline
$ pep263 .
./pep263/core.py: no encoding
./pep263/errors.py: no encoding
./pep263/cli.py: no encoding
...
```

Appending encodings
-------------------------
```commandline
$ pep263 . --append utf-8
./pep263/core.py: utf-8
./pep263/errors.py: utf-8
./pep263/cli.py: utf-8
...
```

Overwriting encodings
---------------------
```commandline
$ pep263 . --append utf-16 --force
./pep263/core.py: utf-16
./pep263/errors.py: utf-16
./pep263/cli.py: utf-16
...
```

License
======
MIT
