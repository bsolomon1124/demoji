# -*- coding: utf-8 -*-

"""Find and replace emojis within text strings.

The set of emojis is refreshable from its canonical source at
http://www.unicode.org/emoji/charts/full-emoji-list.html.
"""

from __future__ import unicode_literals
from __future__ import print_function

__all__ = ("findall", "replace", "last_downloaded_timestamp")
__version__ = "0.0.2"

import datetime
import json
import logging
import os.path
import re
import time

import requests

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging

# Download endpoint
URL = "http://unicode.org/Public/emoji/12.0/emoji-test.txt"

# Host location for this repo
REPO = "https://github.com/bsolomon1124/demoji/issues"

# Directory location for cached downloaded codes
DIRECTORY = os.path.join(os.path.expanduser("~"), ".demoji/")

# Filepath of the cached downloaded codes
CACHEPATH = os.path.join(DIRECTORY, "codes.json")

_zero = datetime.timedelta(0)


class UTC(datetime.tzinfo):
    """UTC (Python 2 compat)"""

    def utcoffset(self, dt):
        return _zero

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _zero


utc = UTC()
del UTC


def _raw_stream_unicodeorg_emojifile(url):
    print("\033[33m" + "Downloading emoji data ..." + "\033[0m")
    resp = requests.request("GET", url, stream=True)
    print(
        "\033[92m"
        + "... OK"
        + "\033[0m"
        + " (Got response in %0.2f seconds)" % resp.elapsed.total_seconds()
    )

    POUNDSIGN = b"#"
    SEMICOLON = b";"
    SPACE = b" "
    for line in resp.iter_lines():
        if not line or line.startswith(POUNDSIGN):
            continue
        codes, desc = line.split(SEMICOLON, maxsplit=1)
        _, desc = desc.split(POUNDSIGN, maxsplit=1)
        *_, desc = desc.split(SPACE, maxsplit=2)
        yield (codes.strip().decode("utf-8"), desc.strip().decode("utf-8"))


def parse_unicode_sequence(string):
    return "".join((chr(int(i.zfill(8), 16)) for i in string.split()))


def parse_unicode_range(string):
    start, _, end = string.partition("..")
    start, end = map(lambda i: int(i.zfill(8), 16), (start, end))
    return (chr(i) for i in range(start, end + 1))


def stream_unicodeorg_emojifile(url=URL):
    for codes, desc in _raw_stream_unicodeorg_emojifile(url):
        if ".." in codes:
            for cp in parse_unicode_range(codes):
                yield cp, desc
        else:
            yield parse_unicode_sequence(codes), desc


def _compile_codes(codes):
    # Expensive, but we need to be very careful because it's likely
    # that 1-2 chars may not compile; see the sequence [42, 65039, 8419]
    # for an example.
    ok = []
    _compile = re.compile
    _error = re.error
    append = ok.append
    for c in sorted(codes, key=len, reverse=True):
        try:
            _compile(c)
        except _error:
            pass
        else:
            append(c)
    return _compile("|".join(ok))


_EMOJI_PAT = None
_CODE_TO_DESC = {}


def download_codes():
    global _EMOJI_PAT
    global _CODE_TO_DESC
    codes = dict(stream_unicodeorg_emojifile(URL))
    _write_codes(codes)
    _EMOJI_PAT = _compile_codes(codes)
    _CODE_TO_DESC.update(codes)


def _write_codes(codes):
    try:
        os.makedirs(DIRECTORY)
    except OSError:
        pass
    print("\033[33m" + "Writing emoji data to %s ..." % CACHEPATH + "\033[0m")
    with open(CACHEPATH, "w") as f:
        json.dump({"timestamp": time.time(), "codes": codes}, f)
    print("\033[92m" + "... OK" + "\033[0m")


def last_downloaded_timestamp():
    try:
        ts, _ = _load_codes_from_file()
        return ts
    except FileNotFoundError:
        return None


def _load_codes_from_file():
    """
    :rtype: tuple
    """
    with open(CACHEPATH) as f:
        data = json.load(f)
        ts = datetime.datetime.fromtimestamp(data["timestamp"])
        codes = data["codes"]
        return ts.replace(tzinfo=utc), codes


def set_emoji_pattern():
    """Get global pattern, or set it if it is None, and return it."""
    global _EMOJI_PAT
    global _CODE_TO_DESC
    if _EMOJI_PAT is None:
        try:
            _, codes = _load_codes_from_file()
        except FileNotFoundError:
            raise FileNotFoundError(
                "No cached data found at %s. First, download"
                " codes locally using `demoji.download_codes()`" % CACHEPATH
            )
        else:
            _EMOJI_PAT = _compile_codes(codes)
            _CODE_TO_DESC.update(codes)


def findall(string):
    set_emoji_pattern()
    return {f: _CODE_TO_DESC[f] for f in set(_EMOJI_PAT.findall(string))}


def replace(string, repl=""):
    set_emoji_pattern()
    return _EMOJI_PAT.sub(repl, string)
