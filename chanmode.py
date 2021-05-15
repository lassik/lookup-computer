#! /usr/bin/env python3

import re

import yaml  # pip3 install pyyaml

import util


GITHUB = "https://raw.githubusercontent.com/"
URL = GITHUB + "ircdocs/irc-defs/gh-pages/_data/chanmodes.yaml"
CACHE = "chanmodes.yaml"
COLUMNS = ["Char", "Name", "Origin", "Comment"]


def scrape_all():
    with open(util.get_cache_file(CACHE, URL), "r") as file:
        data = yaml.safe_load(file)
        for mode in data["values"]:
            char = mode.get("char", "")
            name = mode.get("name", "")
            origin = mode.get("origin", "")
            comment = mode.get("comment", "")
            yield char, name, origin, comment


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape_all())
