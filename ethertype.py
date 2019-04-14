#! /usr/bin/env python3

import csv
import re

import util


URL = "https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers-1.csv"
CACHE_FILE = "ieee-802-numbers-1.csv"
COLUMNS = ["Hex", "Ethertype"]
HEXRANGE = re.compile(r"^([0-9A-F]+)-([0-9A-F]+)$")


def scrape_all():
    with open(util.get_cache_file(CACHE_FILE, URL), newline="") as csvfile:
        reader = csv.reader(csvfile)
        for header_row in reader:
            break
        for row in reader:
            description = row[4].split("\n", 1)[0].strip()
            typeranges = row[1]
            typerange = HEXRANGE.match(typeranges)
            if typerange:
                mintype = int(typerange.group(1), 16)
                maxtype = int(typerange.group(2), 16)
                for typecode in range(mintype, maxtype + 1):
                    yield "0x{:04X}".format(typecode), description
            else:
                typecode = int(typeranges, 16)
                yield "0x{:04X}".format(typecode), description


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape_all())
