import csv
import os
import shutil
import sys
import urllib.request


def _get_main_filename():
    return sys.modules["__main__"].__file__


def _get_output_filename():
    return os.path.splitext(_get_main_filename())[0] + ".csv"


def _get_cache_filename(cache_file):
    mainfile = _get_main_filename()
    prog = os.path.splitext(os.path.basename(mainfile))[0]
    return os.path.join(os.path.dirname(mainfile), ".cache", prog, cache_file)


def get_cache_file(cache_file, url):
    cache_file = _get_cache_filename(cache_file)
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    if not os.path.exists(cache_file):
        with urllib.request.urlopen(url) as response:
            with open(cache_file, "wb") as output:
                shutil.copyfileobj(response, output)
    return cache_file


def write_csv(header_row, data_rows):
    output_file = _get_output_filename()
    with open(output_file, "w", newline="") as output:
        writer = csv.writer(output, lineterminator="\n")
        writer.writerow(header_row)
        for row in data_rows:
            assert len(row) == len(header_row)
            writer.writerow(row)
