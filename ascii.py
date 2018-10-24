#! /usr/bin/env python3

import unicodedata

import util


COLUMNS = ["Binary", "Octal", "Decimal", "Hex", "Display", "Unicode"]


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
    ]


def scrape_all():
    return [char_row(i) for i in range(128)]


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape_all())
