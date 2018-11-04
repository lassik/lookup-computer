#! /usr/bin/env python3

import json
import re

import util


URL = "https://en.wikipedia.org/w/api.php?action=parse&page=List_of_HTTP_status_codes&prop=wikitext&format=json"
CACHE = "api.json"
COLUMNS = ["Code", "Message"]


def scrape():
    j = json.load(open(util.get_cache_file(CACHE, URL)))
    for line in j["parse"]["wikitext"]["*"].splitlines():
        m = re.match(r"^;\{\{.*?\}\}(\d{3}) (.*?)\s*$", line)
        if m:
            yield m.group(1), m.group(2).replace("[[", "").replace("]]", "")


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
