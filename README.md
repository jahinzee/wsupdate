# wsupdate

A comprehensive and extendable Linux system updater, written in
Python.

Intended for use on Linux desktop installations. Updates Distrobox
containers, Flatpaks, system packages with PackageKit, pipx
packages, and BIOS firmware with fwupd.

- The `update()` function contains the main logic flow of the
  update procedure. You may modify it as you wish.

- This script has no dependencies, outside of the Python standard
  library, meaning it should work almost everywhere where Python
  is installed. I tested this with Python 3.12.1, but you should
  be able any supported version.

## Installation

To install this script, use either `pipx` (recommended) or `pip`.

```
pipx install git+https://github.com/jahinzee/wsupdate.git
```

To uninstall, simply run `pipx uninstall wsupdate` or `pip uninstall wsupdate`.

Alternatively, you can download the `src/wsupdate/__init__.py` file
from this repository, and run the script standalone.

## Usage

```
wsupdate [-h] [-b] [-d] [-p]

options:
  -h, --help    show this help message and exit
  -b, --brief   suppress all command outputs, except highlight messages
  -d, --dryrun  prints out update commands, instead of executing them
  -p, --plain   use header labels instead of ANSI colours
```