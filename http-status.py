#! /usr/bin/env python3

import re

import util


URL = "https://en.wikipedia.org/wiki/List_of_HTTP_status_codes?action=raw"
CACHE = "article.wiki"
COLUMNS = ["Code", "Message"]


def scrape():
    for line in open(util.get_cache_file(CACHE, URL)):
        m = re.match(r"^;\{\{.*?\}\}(\d{3}) (.*?)\s*$", line)
        if m:
            yield m.group(1), m.group(2).replace("[[", "").replace("]]", "")


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
