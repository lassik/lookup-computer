#! /usr/bin/env python3

import csv
import html.parser
import os

import requests


CSS3_URL = "https://www.w3.org/TR/css-color-3/"
CSS3_CACHE = "color-css3.html"

OUTPUT_FILE = "color.csv"
COLUMNS = ["Web", "Hex6", "R,G,B"]


def get_cache_file(cache_file, url):
    cache_file = os.path.join(os.path.dirname(__file__), ".cache", cache_file)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    if not os.path.exists(cache_file):
        r = requests.get(url)
        r.raise_for_status()
        open(cache_file, "w").write(r.text)
    return cache_file


class CSS3SpecificationParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.colors = {}
        self.thiscolor = []
        self.colortablerow = -1

    def handle_starttag(self, tag, attrs):
        if tag == "table" and ("class", "colortable") in attrs:
            self.colortablerow = 0
        elif tag == "tr" and self.colortablerow >= 0:
            self.colortablerow += 1

    def handle_endtag(self, tag):
        if tag == "table":
            self.colortablerow = -1

    def handle_data(self, data):
        if self.colortablerow > 1:
            data = data.strip()
            if data:
                self.thiscolor.append(data)
                if len(self.thiscolor) == 3:
                    self.colors[self.thiscolor[0]] = self.thiscolor[1:]
                    self.thiscolor = []


def scrape_css3():
    parser = CSS3SpecificationParser()
    parser.feed(open(get_cache_file(CSS3_CACHE, CSS3_URL)).read())
    return parser.colors


def scrape_all():
    return [(a, b, c) for a, (b, c) in sorted(scrape_css3().items())]


def write_csv(rows):
    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        wr = csv.writer(csvfile, lineterminator="\n")
        wr.writerow(COLUMNS)
        for row in sorted(rows):
            wr.writerow(row)


if __name__ == "__main__":
    write_csv(scrape_all())
