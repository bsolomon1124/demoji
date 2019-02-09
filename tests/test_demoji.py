from __future__ import unicode_literals

import datetime
import os
import re

import pytest

import demoji

person_tipping_hand = "💁"  # length 1
man_tipping_hand = "💁‍♂️"  # length 4
woman_tipping_hand = "💁‍♀️"  # length 4


def test_setup():
    assert len(person_tipping_hand) == 1
    assert len(man_tipping_hand) == 4
    assert len(woman_tipping_hand) == 4


def test_load_codes_from_file():
    if os.path.isfile(demoji.CACHEPATH):
        os.remove(demoji.CACHEPATH)
    with pytest.raises(FileNotFoundError):
        demoji._load_codes_from_file()
    assert demoji.last_downloaded_timestamp() is None


def test_constants():
    assert demoji.UPAT.search("U+FFFF")
    assert demoji.UPAT.search("U+FFFF00")


def test_compile_codes():
    badmark = "".join((chr(42), chr(65039), chr(8419)))
    assert demoji._compile_codes([badmark]) == re.compile("")
    assert demoji._compile_codes(["a"]) == re.compile("a")
    assert demoji._compile_codes([badmark, "aa", "b"]) == re.compile("aa|b")


def test_last_downloaded_timestamp_rettype():
    ts = demoji.last_downloaded_timestamp()
    assert isinstance(ts, datetime.datetime) or ts is None


def test_utc():
    now = datetime.datetime.utcnow().replace(tzinfo=demoji.utc)
    assert now.utcoffset() == datetime.timedelta(0)


def test_demoji_main():
    demoji.set_emoji_pattern(False)
    assert demoji.findall("Hi") == []
    assert demoji.replace("Hi") == "Hi"
    assert demoji.findall("The 🌓 shall rise again") == ["🌓"]
    allhands = "Someone actually gets paid to make a %s, a %s, and a %s" % (
        person_tipping_hand,
        man_tipping_hand,
        woman_tipping_hand,
    )
    assert demoji.findall(allhands) == [
        person_tipping_hand,
        man_tipping_hand,
        woman_tipping_hand,
    ]
    assert (
        demoji.replace(allhands)
        == "Someone actually gets paid to make a , a , and a "
    )
    assert (
        demoji.replace(allhands, "X")
        == "Someone actually gets paid to make a X, a X, and a X"
    )
    assert isinstance(demoji.last_downloaded_timestamp(), datetime.datetime)
