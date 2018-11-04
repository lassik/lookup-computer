#! /usr/bin/env python3

import re

import util


URL = "https://tools.ietf.org/rfc/index"
CACHE = "rfc.html"
COLUMNS = ["RFC", "Title"]
CROSSLINK = re.compile(r'<a href=".*?">(.*?)(</a>|\.])')
RFC = re.compile(r'<a href="http:..tools.ietf.org.html.\d+">RFC(\d+)</a>\s+(.*)')


def fix_description(s):
    s = CROSSLINK.sub(r"\1", s)
    s = re.sub("\s+", " ", s)
    s = s.strip()
    return s


def scrape():
    current = None
    for line in open(util.get_cache_file(CACHE, URL)).readlines():
        rfc = RFC.match(line)
        desc = None
        if rfc:
            current = [rfc.group(1), ""]
            desc = rfc.group(2)
        elif current:
            desc = line
        if desc:
            pivot = desc.find("(Format:")
            was_last = pivot >= 0
            desc = desc[:pivot] if was_last else desc
            current[1] += desc
            if was_last:
                yield current[0], fix_description(current[1])
                current = None


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
