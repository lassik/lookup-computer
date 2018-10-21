#! /usr/bin/env python3

import csv
import os
import re

import requests


GITHUB = "https://raw.githubusercontent.com"

OS = [
    (
        "Linux",
        [
            "torvalds/linux/master/include/uapi/asm-generic/errno-base.h",
            "torvalds/linux/master/include/uapi/asm-generic/errno.h",
        ],
    ),
    ("FreeBSD", ["freebsd/freebsd/master/sys/sys/errno.h"]),
    ("OpenBSD", ["openbsd/src/master/sys/sys/errno.h"]),
    ("NetBSD", ["netbsd/src/trunk/sys/sys/errno.h"]),
    ("Solaris", ["kofemann/opensolaris/master/usr/src/uts/common/sys/errno.h"]),
]

COLUMNS = ["Name"] + [os[0] for os in OS] + ["Message"]


def scrape_os(os_name, github_path, cache_file, errors={}):
    if not os.path.exists(cache_file):
        r = requests.get(os.path.join(GITHUB, github_path))
        r.raise_for_status()
        open(cache_file, "w").write(r.text)
    for line in open(cache_file):
        match = re.match(
            r"^#define\s+(E[A-Z\d]+)\s+([A-Z\d]+)\s+/\*\s*(.*?)\s*\*/", line
        )
        if match:
            name, code, message = match.group(1), match.group(2), match.group(3)
            errors[name] = errors.get(name, [""] * len(COLUMNS))
            errors[name][COLUMNS.index("Name")] = name
            errors[name][COLUMNS.index("Message")] = message
            errors[name][COLUMNS.index(os_name)] = code
    return errors


def scrape_all():
    errors = {}
    for os_name, github_paths in OS:
        for i, github_path in enumerate(github_paths):
            cache_file = "errno-{}{}.h".format(os_name.lower(), i or "")
            scrape_os(
                os_name,
                github_path,
                os.path.join(os.path.dirname(__file__), cache_file),
                errors,
            )
    return errors


def write_csv(errors):
    with open("errno.csv", "w", newline="") as csvfile:
        wr = csv.writer(csvfile, lineterminator="\n")
        wr.writerow(COLUMNS)
        for _, error in sorted(errors.items()):
            wr.writerow(error)


if __name__ == "__main__":
    write_csv(scrape_all())
