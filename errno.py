#! /usr/bin/env python3

import re

import util


GITHUB = "https://raw.githubusercontent.com/"

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
    ("Darwin", ["apple/darwin-xnu/master/bsd/sys/errno.h"]),
]

COLUMNS = ["Name"] + [os[0] for os in OS] + ["Message"]
DEFINE = re.compile(r"^#define\s+(E[A-Z\d]+)\s+([A-Z\d]+)\s+/\*\s*(.*?)\s*\*/")


def scrape_os(os_name, github_path, cache_file, errors={}):
    for line in open(util.get_cache_file(cache_file, GITHUB + github_path)):
        define = DEFINE.match(line)
        if define:
            name, code, message = define.group(1), define.group(2), define.group(3)
            errors[name] = errors.get(name, [""] * len(COLUMNS))
            errors[name][COLUMNS.index("Name")] = name
            errors[name][COLUMNS.index("Message")] = message
            errors[name][COLUMNS.index(os_name)] = code
    return errors


def scrape_all():
    errors = {}
    for os_name, github_paths in OS:
        for i, github_path in enumerate(github_paths):
            cache_file = "{}{}.h".format(os_name.lower(), i or "")
            scrape_os(os_name, github_path, cache_file, errors)
    return [row for _, row in sorted(errors.items())]


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape_all())
