#! /usr/bin/env python3

import html.parser

import util


CACHE = "msdn.html"
URL = "https://docs.microsoft.com/en-us/windows/desktop/winsock/windows-sockets-error-codes-2"

COLUMNS = ["Name", "Code", "Message"]


def fixup(row):
    if row[0] == "WSA_IO_PENDING":
        return row + ["Overlapped operations will complete later."]
    return row


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_dt = False
        self.rows = []
        self.row = []

    def handle_starttag(self, tag, attrs):
        if tag == "dt":
            self.in_dt = True

    def handle_endtag(self, tag):
        if tag == "dt":
            self.in_dt = False

    def handle_data(self, data):
        is_first = data.startswith("WS")
        if self.in_dt:
            if len(self.row) == 3 or (self.row and is_first):
                self.rows.append(fixup(self.row))
                self.row = []
            if is_first or self.row:
                self.row.append(data)


def scrape():
    parser = Parser()
    parser.feed(open(util.get_cache_file(CACHE, URL)).read())
    return parser.rows


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
