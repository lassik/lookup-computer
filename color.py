#! /usr/bin/env python3

import html.parser

import util


CSS3_URL = "https://www.w3.org/TR/css-color-3/"
CSS3_CACHE = "color-css3.html"

COLUMNS = ["Web", "Hex6", "R,G,B"]


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
    parser.feed(open(util.get_cache_file(CSS3_CACHE, CSS3_URL)).read())
    return parser.colors


def scrape_all():
    return [(a, b, c) for a, (b, c) in sorted(scrape_css3().items())]


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape_all())
