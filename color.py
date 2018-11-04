#! /usr/bin/env python3

import html.parser

import util


URL = "https://www.w3.org/TR/css-color-3/"
CACHE = "color-css3.html"
COLUMNS = ["Web", "Hex6", "R,G,B"]


class Parser(html.parser.HTMLParser):
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


def scrape():
    parser = Parser()
    parser.feed(open(util.get_cache_file(CACHE, URL)).read())
    return [(a, b, c) for a, (b, c) in sorted(parser.colors.items())]


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
