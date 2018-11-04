#! /usr/bin/env python3

import re

import util


URL = "https://tools.ietf.org/rfc/index"
CACHE = "rfc.html"
COLUMNS = ["RFC", "Title"]
CROSSLINK = re.compile(r'<a href=".*?">(.*?)(</a>|\.])')
RFC = re.compile(
    r'<a href="http:..tools.ietf.org.html.\d+">RFC(\d+)</a>\s+(.*?)\s*\(Format:'
)


def scrape():
    for line in open(util.get_cache_file(CACHE, URL)).readlines():
        rfc = RFC.match(line)
        if rfc:
            yield rfc.group(1), CROSSLINK.sub(r"\1", rfc.group(2))


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
