#! /usr/bin/env python3

import html.parser

import util


URL = "https://docs.microsoft.com/en-us/windows/desktop/winsock/windows-sockets-error-codes-2"
CACHE = "msdn.html"
COLUMNS = ["Name", "Code", "Message"]


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
        if self.in_dt:
            if len(self.row) == 2 and self.row[0] == "WSA_IO_PENDING":
                self.row.append("Overlapped operations will complete later.")
            if len(self.row) == 3:
                self.rows.append(self.row)
                self.row = []
            if self.row or data.startswith("WS"):
                self.row.append(data)


def scrape():
    parser = Parser()
    parser.feed(open(util.get_cache_file(CACHE, URL)).read())
    return parser.rows


if __name__ == "__main__":
    util.write_csv(COLUMNS, scrape())
