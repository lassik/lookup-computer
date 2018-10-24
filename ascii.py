#! /usr/bin/env python3

import re
import tarfile
import unicodedata

import util


TARSTEM = "ascii-3.18"
TARFILE = TARSTEM + ".tar.gz"
URL = "http://www.catb.org/~esr/ascii/" + TARFILE

COLUMNS = ["Binary", "Octal", "Decimal", "Hex", "Display", "Unicode", "Slang"]


def slang_names():
    slang = [""] * 128
    field = None
    i = 0
    for line in (
        tarfile.open(util.get_cache_file(TARFILE, URL))
        .extractfile(TARSTEM + "/nametable")
        .read()
        .decode("ascii")
        .splitlines()
    ):
        if line == "%%":
            i += 1
            continue
        m = re.match(r"^([A-Za-z]+):\s*(.*?)\s*$", line)
        if m:
            field = m.group(1)
            value = m.group(2)
        m = re.match(r"^\s+(.*?)\s*$", line)
        if m:
            value = m.group(1)
        if field == "Synonyms":
            slang[i] += value
    for i in range(len(slang)):
        fields = re.sub(r'["]', " ", slang[i]).split(",")
        slang[i] = " / ".join(filter(None, map(str.strip, fields)))
    return slang


def slang_name(i):
    return slang_names()[i]


def unicode_name(i):
    # Python's unicodedata doesn't have control character names :-(
    if i < 0x20:
        return ""
    if i == 0x7f:
        return ""
    return unicodedata.name(u"" + chr(i))


def display(i):
    if i < 0x20:
        return "^" + chr(ord("@") + i)
    if i == 0x7f:
        return "^?"
    return chr(i)


def char_row(i):
    return [
        "0b{:08b}".format(i),
        "0o{:03o}".format(i),
        "{:d}".format(i),
        "0x{:02x}".format(i),
        display(i),
        unicode_name(i),
        slang_name(i),
    ]


def scrape_all():
    return [char_row(i) for i in range(128)]


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape_all())
