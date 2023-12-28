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

To uninstall, simply run `pipx uninstall wsupdate` or
`pip uninstall wsupdate`.

Alternatively, you can download the `src/wsupdate/__init__.py`
file from this repository, and run the script standalone.

## Usage

```
usage: wsupdate [-h] [-b] [-d] [-p] [-r] [-R] [-P]

options:
  -h, --help            show this help message and exit
  -b, --brief           suppress all command outputs, except highlight
                        messages
  -d, --dryrun          prints out update commands, instead of executing them
  -p, --plain           use header labels instead of ANSI colours
  -r, --update-arch     update Arch Linux and AUR packages (EXPERIMENTAL)
                        (will be ignored if not on Arch Linux)
  -R, --skip-arch-warning
                        skip Arch Linux experimental warning, use with
                        --update-arch (will be ignored if not on Arch Linux)
  -P, --use-pkcon-on-arch
                        allow PackageKit updates on Arch Linux (will be
                        ignored if not on Arch Linux)
```

### EXPERIMENTAL: Arch Linux Updater

To run the Arch Linux updater, use the flag `--update-arch`.

The Arch Linux updater is in an *experimental* stage, and has not been
thoroughly tested. **Your system may be in an unstable state if used
improperly**. It is strongly recommended that you use
`wsupdate --dryrun` to validate command outputs before committing to
an update.

> "Users must be vigilant and take responsibility for maintaining their own system."
> -- [Arch Linux Wiki](https://wiki.archlinux.org/title/System_maintenance#Upgrading_the_system)

**Note:** PackageKit updates are disabled on Arch Linux by default,
as it has been [reported to be unreliable](https://www.reddit.com/r/archlinux/comments/139f49o/hows_packagekit_support_nowadays/jj39otc/).
To remove this restriction, use the flag `--use-pkcon-on-arch`.