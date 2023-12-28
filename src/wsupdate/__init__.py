#!/usr/bin/python

"""
wsupdate - A comprehensive and extendable Linux system updater,
written in Python.

Copyright (c) 2023 - 2024 by Jahin Z. <jahinzee@outlook.com>

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import shutil, subprocess, platform, argparse


def get_subprocess_function(brief, dryrun):
    if dryrun:

        def dryrun(s):
            print(f"# {' '.join(s)}")
            return 0

        return dryrun
    if brief:

        def quietrun(s):
            return subprocess.run(
                s, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            ).returncode

        return quietrun
    if True:

        def run(s):
            return subprocess.run(s).returncode

        return run


def get_log_function(plain):
    if plain:

        def plainlog(message, mode):
            print(f"{mode}\t :: {message}")

        return plainlog

    if True:

        def colourlog(message, mode):
            MODES = {"ERROR": 1, "OK": 2, "WARN": 3, "INFO": 4, "SECTION": 7}
            BOLD = "\033[1m"
            RESET = "\033[0m"
            print(f"{BOLD}\033[1;3{MODES.get(mode, 7)}m:: {message}{RESET}")

        return colourlog


def get_args():
    parser = argparse.ArgumentParser(
        prog="wsupdate",
        description="A comprehensive and extendable Linux system updater, written in Python.",
    )
    parser.add_argument(
        "-b",
        "--brief",
        action="store_true",
        help="suppress all command outputs, except highlight messages",
    )
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_true",
        help="prints out update commands, instead of executing them",
    )
    parser.add_argument(
        "-p",
        "--plain",
        action="store_true",
        help="use header labels instead of ANSI colours",
    )
    return parser.parse_args()


def log(message, mode):
    MODES = {"ERROR": 1, "OK": 2, "WARN": 3, "INFO": 4, "SECTION": 7}
    BOLD = "\033[1m"
    RESET = "\033[0m"
    print(f"{BOLD}\033[1;3{MODES.get(mode, 7)}m:: {message}{RESET}")


def binary_exists(name: str) -> bool:
    return shutil.which(name) is not None


def update_flatpak(run, log, system, user):
    if not binary_exists("flatpak"):
        log("Flatpak not available, skipping...", "WARN")
        return
    log("Updating Flatpak applications...", "SECTION")
    system_flag = "--system" if system else ""
    user_flag = "--user" if user else ""
    run(["flatpak", "upgrade", "-y", system_flag, user_flag])


def update_distrobox(run, log):
    if not binary_exists("distrobox"):
        log("Distrobox not available, skipping...", "WARN")
        return
    log("Updating Distrobox containers...", "SECTION")
    run(["distrobox", "upgrade", "--all"])


def update_packagekit(run, log, offline):
    if not binary_exists("pkcon"):
        log("PackageKit (pkcon) not available, skipping...", "ERROR")
        return
    log("Updating system packages with PackageKit...", "SECTION")
    offline_flag = "-d" if offline else ""
    run(["pkcon", "update", offline_flag, "-y"])
    if offline:
        restart_required = run(["pkcon", "offline-trigger"]) == 0
        if restart_required:
            log("System packages will be updated on next boot.", "INFO")


def update_firmware(run, log):
    if not binary_exists("fwupdmgr"):
        log("fwupd not available, skipping...", "WARN")
        return
    log("Updating system firmware with fwupd...", "SECTION")
    run(["fwupdmgr", "refresh"])
    updates_available = run(["fwupdmgr", "get-updates"]) == 0
    if updates_available:
        run(["fwupdmgr", "update"])
    log(
        "Firmware updates may require a restart. Read the above logs for more information.",
        "INFO",
    )


def update_pipx(run, log):
    if not binary_exists("pipx"):
        log("pipx not available, skipping...", "WARN")
        return
    log("Updating pipx applications...", "SECTION")
    run(["pipx", "upgrade-all"])


def update(run, log):
    # Modify this function to customise the update procedure
    update_flatpak(run, log, system=True, user=True)
    update_distrobox(run, log)
    update_pipx(run, log)
    update_packagekit(run, log, offline=True)
    update_firmware(run, log)


def main():
    arguments = get_args()
    if platform.system() != "Linux":
        log(
            "This script is designed to run only on Linux-based systems.",
            "ERROR",
        )
        exit(1)
    run = get_subprocess_function(arguments.brief, arguments.dryrun)
    log = get_log_function(arguments.plain)
    update(run, log)
    log("Upgrade complete!", "OK")


if __name__ == "__main__":
    main()
