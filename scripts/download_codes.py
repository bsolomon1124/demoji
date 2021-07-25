#!/usr/bin/env python3

"""Download emoji data to package_data."""

import datetime
import json
import pathlib
import re
import time

import colorama
import requests

from demoji import URL

# We do *not* use importlib.resources here since we just want the source file,
# not where it (might) be instlled
parent = pathlib.Path(__file__).parent.parent.resolve() / "demoji"
CACHEPATH = parent / "codes.json"
MODULEPATH = parent / "__init__.py"


def download_codes(dest=CACHEPATH):
    codes = dict(stream_unicodeorg_emojifile(URL))
    _write_codes(codes, CACHEPATH)


def _write_codes(codes, dest):
    print(
        colorama.Fore.YELLOW
        + "Writing emoji data to %s ..." % CACHEPATH
        + colorama.Style.RESET_ALL
    )
    with open(CACHEPATH, "w") as f:
        json.dump(codes, f, separators=(",", ":"))
    print(colorama.Fore.GREEN + "... OK" + colorama.Style.RESET_ALL)


def stream_unicodeorg_emojifile(url=URL):
    for codes, desc in _raw_stream_unicodeorg_emojifile(url):
        if ".." in codes:
            for cp in parse_unicode_range(codes):
                yield cp, desc
        else:
            yield parse_unicode_sequence(codes), desc


def parse_unicode_sequence(string):
    return "".join((chr(int(i.zfill(8), 16)) for i in string.split()))


def parse_unicode_range(string):
    start, _, end = string.partition("..")
    start, end = map(lambda i: int(i.zfill(8), 16), (start, end))
    return (chr(i) for i in range(start, end + 1))


def _raw_stream_unicodeorg_emojifile(url):
    colorama.init()
    print(
        colorama.Fore.YELLOW
        + "Downloading emoji data from %s ..." % URL
        + colorama.Style.RESET_ALL
    )
    resp = requests.request("GET", url, stream=True)
    print(
        colorama.Fore.GREEN
        + "... OK"
        + colorama.Style.RESET_ALL
        + " (Got response in %0.2f seconds)" % resp.elapsed.total_seconds()
    )

    POUNDSIGN = "#"
    POUNDSIGN_B = b"#"
    SEMICOLON = ";"
    SPACE = " "
    for line in resp.iter_lines():
        if not line or line.startswith(POUNDSIGN_B):
            continue
        line = line.decode("utf-8")
        codes, desc = line.split(SEMICOLON, 1)
        _, desc = desc.split(POUNDSIGN, 1)
        desc = desc.split(SPACE, 3)[-1]
        yield (codes.strip(), desc.strip())


def replace_lastdownloaded_timestamp():
    with open(MODULEPATH) as f:
        text = f.read()
    now = datetime.datetime.fromtimestamp(
        time.time(), tz=datetime.timezone.utc
    )
    ldt_re = re.compile(r"^_LDT = .*$", re.M)
    with open(MODULEPATH, "w") as f:
        f.write(ldt_re.sub("_LDT = %r  # noqa: E501" % now, text))
    print(
        colorama.Fore.GREEN
        + "Replaced timestamp with %r in %s" % (now, MODULEPATH)
        + colorama.Style.RESET_ALL
    )


if __name__ == "__main__":
    download_codes()
    replace_lastdownloaded_timestamp()
