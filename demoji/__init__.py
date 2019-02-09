#!/usr/bin/env python

"""Find and replace emojis within text strings.

The set of emojis is refreshable from its canonical source at
http://www.unicode.org/emoji/charts/full-emoji-list.html.
"""

from __future__ import unicode_literals

__all__ = ("findall", "replace", "last_downloaded_timestamp")
__version__ = "0.0.2"

import datetime
import json
import logging
import os.path
import re
import time

import bs4
import requests

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging

# U+XXXX style codes
UPAT = re.compile(r"U\+[A-Z\d]+")

# Download location
BASE_URL = "http://www.unicode.org/emoji/charts/full-emoji-list.html"

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


def _download_codes():
    """
    :rtype: set
    """
    print(
        "\033[33m" + "Downloading emoji data to %s ..." % CACHEPATH + "\033[0m"
    )
    resp = requests.request("GET", BASE_URL, verify=False)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(
            "Downloading Unicode code points from %s returned a bad status"
            " code: %d\nIf this problem persists, please file an Issue"
            " at %s" % (BASE_URL, resp.status_code, REPO)
        ) from e
    print("\033[92m" + "... DONE" + "\033[0m")
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    tags = soup.find_all("td", attrs={"class": "code"})
    codes = set()
    codesadd = codes.add
    join = "".join
    for tag in tags:
        found = UPAT.findall(tag.get_text())
        # The join is for *sequence emojis*.  For example,
        # - U+1F646 is "person gesturing OK"
        # - U+1F646 U+200D U+2642 U+FE0F is "man gesturing OK"
        # - U+1F646 U+200D U+2640 U+FE0F is "woman gesturing OK"
        # For more, see:
        # http://www.unicode.org/emoji/charts/emoji-sequences.html
        codesadd(join((chr(int(i[2:].zfill(8), 16)) for i in found)))
    return codes


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


def _write_codes(codes):
    try:
        os.makedirs(DIRECTORY)
    except OSError:
        pass
    with open(CACHEPATH, "w") as f:
        json.dump({"timestamp": time.time(), "codes": tuple(codes)}, f)


def download_codes():
    codes = _download_codes()
    _write_codes(codes)
    return codes


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


_EMOJI_PAT = None


def set_emoji_pattern(use_cache):
    """Get global pattern, or set it if it is None, and return it."""
    global _EMOJI_PAT
    if use_cache:
        if _EMOJI_PAT is None:
            try:
                _, codes = _load_codes_from_file()
            except FileNotFoundError:
                download_codes()
                _, codes = _load_codes_from_file()
            _EMOJI_PAT = _compile_codes(codes)
    else:
        download_codes()
        _, codes = _load_codes_from_file()
        _EMOJI_PAT = _compile_codes(codes)


set_emoji_pattern(True)


def findall(string, use_cache=True):
    set_emoji_pattern(use_cache)
    return _EMOJI_PAT.findall(string)


def replace(string, repl="", use_cache=True):
    set_emoji_pattern(use_cache)
    return _EMOJI_PAT.sub(repl, string)
