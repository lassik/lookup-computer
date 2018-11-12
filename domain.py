#! /usr/bin/env python3

import re

import util


URL = "https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains?action=raw"
CACHE = "article.wiki"
COLUMNS = ["Domain", "Description"]


def cleanup_table_column(s):
    s = s.strip()
    s = re.sub(r"\[\[(.*?)(\|.*?)?\]\]", r"\1", s)
    s = re.sub(r"\{\{flag\|(.*?)\}\}", r"\1", s)
    s = re.sub(r"<.*", "", s)
    s = s.strip()
    return s


def scrape():
    for line in open(util.get_cache_file(CACHE, URL)):
        if re.match(r"\| \[\[\.[a-z]+\]\] \|\|", line):
            columns = line[1:].split("||")
            yield list(map(cleanup_table_column, columns[:2]))


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
