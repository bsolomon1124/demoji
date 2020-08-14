# -*- coding: utf-8 -*-

"""Find and replace emojis within text strings.

The set of emojis is refreshable from its canonical source at
http://www.unicode.org/emoji/charts/full-emoji-list.html.
"""

from __future__ import unicode_literals
from __future__ import print_function

__all__ = ("findall", "replace", "last_downloaded_timestamp")
__version__ = "0.2.2-dev0"

import datetime
import json
import logging
import os.path
import re
import sys
import time

import colorama
import requests

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging

PY2 = sys.version_info[0] == 2
if PY2:
    # On a narrow build (the default), we will get
    # ValueError: unichr() arg not in range(0x10000) (narrow Python build)
    # for any code points above this range.  Internally, they will be
    # stored as a UTF-16 surrogate pair
    import struct

    def chr(i):
        try:
            return unichr(i)
        except ValueError:
            return struct.pack("i", i).decode("utf-32")
else:
    chr = chr

del sys

# Download endpoint
URL = "http://unicode.org/Public/emoji/12.0/emoji-test.txt"

# Directory location for cached downloaded codes
DIRECTORY = os.path.join(os.path.expanduser("~"), ".demoji")

# Filepath of the cached downloaded codes
CACHEPATH = os.path.join(DIRECTORY, "codes.json")

_zero = datetime.timedelta(0)


class UTC(datetime.tzinfo):
    """UTC (Python 2 compat)."""

    def utcoffset(self, dt):
        return _zero

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return _zero


utc = UTC()
del UTC


def _raw_stream_unicodeorg_emojifile(url):
    colorama.init()
    print(
        colorama.Fore.YELLOW
        + "Downloading emoji data ..."
        + colorama.Style.RESET_ALL
    )
    resp = requests.request("GET", url, stream=True)
    print(
        colorama.Fore.GREEN
        + "... OK"
        + colorama.Style.RESET_ALL
        + " (Got response in %0.2f seconds)" % resp.elapsed.total_seconds()
    )

    POUNDSIGN = b"#"
    SEMICOLON = b";"
    SPACE = b" "
    for line in resp.iter_lines():
        if not line or line.startswith(POUNDSIGN):
            continue
        codes, desc = line.split(SEMICOLON, 1)
        _, desc = desc.split(POUNDSIGN, 1)
        desc = desc.split(SPACE, 2)[-1]
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
    escp = (re.escape(c) for c in sorted(codes, key=len, reverse=True))
    return re.compile(r"|".join(escp))


_EMOJI_PAT = None
_CODE_TO_DESC = {}


def download_codes():
    """Download emoji data to ~/.demoji/codes.json.

    This will also set the global module variables _EMOJI_PAT and
    _CODE_TO_DESC, which are a regex and dictionary, respectively.
    """

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
    print(
        colorama.Fore.YELLOW
        + "Writing emoji data to %s ..." % CACHEPATH
        + colorama.Style.RESET_ALL
    )
    with open(CACHEPATH, "w") as f:
        json.dump({"timestamp": time.time(), "codes": codes}, f)
    print(
        colorama.Fore.GREEN
        + "... OK"
        + colorama.Style.RESET_ALL
    )


def last_downloaded_timestamp():
    try:
        ts, _ = _load_codes_from_file()
        return ts
    except IOError:
        return None


def _load_codes_from_file():
    with open(CACHEPATH) as f:
        data = json.load(f)
        ts = datetime.datetime.fromtimestamp(data["timestamp"])
        codes = data["codes"]
        return ts.replace(tzinfo=utc), codes


def set_emoji_pattern():
    global _EMOJI_PAT
    global _CODE_TO_DESC
    if _EMOJI_PAT is None:
        try:
            _, codes = _load_codes_from_file()
        except IOError:
            raise IOError(
                "No cached data found at %s. First, download"
                " codes locally using `demoji.download_codes()`" % CACHEPATH
            )
        else:
            _EMOJI_PAT = _compile_codes(codes)
            _CODE_TO_DESC.update(codes)


def findall(string):
    """Find emojis within ``string``.

    :param string: The input text to search
    :type string: str
    :return: A dictionary of ``{emoji: description}``
    :rtype: dict
    """

    set_emoji_pattern()
    return {f: _CODE_TO_DESC[f] for f in set(_EMOJI_PAT.findall(string))}


def replace(string, repl=""):
    """Replace emojis in ``string`` with ``repl``.

    :param string: The input text to search
    :type string: str
    :return: Modified ``str`` with replacements made
    :rtype: str
    """
    set_emoji_pattern()
    return _EMOJI_PAT.sub(repl, string)


def findall_list(string):
    """Find emojis within ``string`` like findall() but returns a list with each occurrence instead of dictionary. 
    Useful for looping through. Added by David Agudelo (@davidagud)

    :param string: The input text to search
    :type string: str
    :return: A list of ``[emoji: description]``
    :rtype: list
    """
    
    set_emoji_pattern()

    return [_CODE_TO_DESC[f] for f in list(_EMOJI_PAT.findall(string))]


def replace_w_desc(string):
    """Replace emojis in ``string`` with their description.
    Added by David Agudelo (@davidagud)

    :param string: The input text to search
    :type string: str
    :return: Modified ``str`` with replacements made
    :rtype: str
    """

    set_emoji_pattern()

    emoji_dict = findall(string)

    updated_string = string

    for emoji in emoji_dict:
        updated_string = string.replace(emoji, ':' + emoji_dict[emoji] + ':')

    return updated_string
