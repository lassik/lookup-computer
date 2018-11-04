#! /usr/bin/env python3

import json
import re

import util


URL = "https://en.wikipedia.org/w/api.php?action=parse&prop=wikitext&format=json&page=List_of_Internet_top-level_domains"
CACHE = "api.json"
COLUMNS = ["Domain", "Description"]


def cleanup_table_column(s):
    s = s.strip()
    s = re.sub(r"\[\[(.*?)(\|.*?)?\]\]", r"\1", s)
    s = re.sub(r"\{\{flag\|(.*?)\}\}", r"\1", s)
    s = re.sub(r"<.*", "", s)
    s = s.strip()
    return s


def scrape():
    j = json.load(open(util.get_cache_file(CACHE, URL)))
    for line in j["parse"]["wikitext"]["*"].splitlines():
        if re.match(r"\| \[\[\.[a-z]+\]\] \|\|", line):
            columns = line[1:].split("||")
            yield list(map(cleanup_table_column, columns[:2]))


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
